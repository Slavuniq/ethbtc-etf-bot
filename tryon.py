import asyncio, logging, os, shutil, uuid, tempfile, time, traceback
from PIL import Image
from gradio_client import Client, handle_file
import httpx
import config

logger = logging.getLogger(__name__)

JP = {
    "necklace": "wearing a beautiful elegant necklace, photorealistic fashion photo",
    "earrings": "wearing stylish earrings, photorealistic portrait",
    "bracelet": "wearing an elegant bracelet, fashion photo",
    "ring": "wearing a beautiful ring, close-up fashion photo",
    "watch": "wearing a luxury wristwatch, fashion editorial",
    "glasses": "wearing stylish sunglasses, photorealistic portrait",
}

# ---------- fallback HF spaces ----------

CLOTHES_SPACES = [
    config.HF_TRYON_SPACE,       # yisol/IDM-VTON
    "Nymbo/Virtual-Try-On",
    "BestWishYsh/IDM-VTON",
    "Xenova/IDM-VTON",
]

JEWELRY_SPACES = [
    config.HF_JEWELRY_SPACE,     # multimodalart/stable-diffusion-inpainting
    "runwayml/stable-diffusion-inpainting",
]

# ---------- image preprocessing ----------

def _prepare_image(path: str, target_w: int, target_h: int) -> str:
    """Resize image to target dimensions using LANCZOS, save as PNG temp file."""
    img = Image.open(path).convert("RGB")
    img = img.resize((target_w, target_h), Image.LANCZOS)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name, format="PNG", quality=100)
    tmp.close()
    return tmp.name


# ---------- result resolver ----------

def _resolve_result(res) -> str | None:
    """Extract a usable file path or URL from various gradio result formats."""
    logger.info(f"[VTON] Raw result type={type(res).__name__}, value={str(res)[:500]}")

    # Unwrap list/tuple — take first element
    if isinstance(res, (list, tuple)):
        if len(res) == 0:
            return None
        res = res[0]

    # Dict with path/url/image keys
    if isinstance(res, dict):
        for key in ("path", "url", "image", "name"):
            val = res.get(key)
            if val:
                res = val
                break
        else:
            logger.warning(f"[VTON] Dict result has no usable key: {res.keys()}")
            return None

    # At this point res should be a string
    if not isinstance(res, str):
        logger.warning(f"[VTON] Unexpected result type after unwrap: {type(res)}")
        return None

    # If it's a local file path that exists — use it directly
    if os.path.exists(res):
        return res

    # If it looks like a URL — download it
    if res.startswith("http://") or res.startswith("https://"):
        return _download_url(res)

    logger.warning(f"[VTON] Result string is neither a file nor URL: {res[:200]}")
    return None


def _download_url(url: str) -> str | None:
    """Download image from URL to a temp file."""
    try:
        logger.info(f"[VTON] Downloading result from URL: {url[:200]}")
        with httpx.Client(timeout=60, follow_redirects=True) as client:
            resp = client.get(url)
            resp.raise_for_status()
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        tmp.write(resp.content)
        tmp.close()
        # Verify it's a valid image
        img = Image.open(tmp.name)
        img.verify()
        return tmp.name
    except Exception as e:
        logger.error(f"[VTON] Failed to download URL: {e}")
        return None


# ---------- clothes try-on ----------

async def run_clothes_tryon(pp: str, gp: str):
    def _r():
        # Prepare images: IDM-VTON expects 768x1024
        prep_pp = _prepare_image(pp, 768, 1024)
        prep_gp = _prepare_image(gp, 768, 1024)

        for sp in CLOTHES_SPACES:
            for attempt in range(2):  # 1 retry per space
                try:
                    logger.info(f"[VTON] Trying space: {sp} (attempt {attempt + 1})")
                    c = Client(sp, hf_token=None)
                    res = c.predict(
                        dict={"background": handle_file(prep_pp), "layers": [], "composite": None},
                        garm_img=handle_file(prep_gp),
                        garment_des="a garment, high quality fashion photo",
                        is_checked=True,
                        is_checked_crop=True,
                        denoise_steps=50,
                        seed=42,
                        api_name="/tryon",
                    )
                    resolved = _resolve_result(res)
                    if resolved:
                        logger.info(f"[VTON] Success with {sp}")
                        return _save_result(resolved)
                    else:
                        logger.warning(f"[VTON] {sp} returned empty/invalid result")
                except Exception as e:
                    logger.error(f"[VTON] {sp} attempt {attempt + 1} failed: {e}")
                    logger.debug(traceback.format_exc())
                    if attempt == 0:
                        time.sleep(5)  # Wait before retry
                    continue

        # All spaces failed — log summary
        logger.error("[VTON] All clothes try-on spaces failed!")
        return None

    return await asyncio.to_thread(_r)


# ---------- jewelry try-on ----------

async def run_jewelry_tryon(pp: str, jp: str, jt: str = "necklace"):
    pr = JP.get(jt, f"wearing a {jt}, photorealistic")

    def _r():
        prep_pp = _prepare_image(pp, 512, 512)

        for sp in JEWELRY_SPACES:
            for attempt in range(2):
                try:
                    logger.info(f"[Jewelry] Trying space: {sp} (attempt {attempt + 1})")
                    c = Client(sp, hf_token=None)
                    res = c.predict(
                        prompt=pr,
                        negative_prompt="blurry,deformed,ugly",
                        image=handle_file(prep_pp),
                        mask_image=handle_file(prep_pp),
                        steps=35,
                        guidance_scale=8.5,
                        strength=0.4,
                        api_name="/infer",
                    )
                    resolved = _resolve_result(res)
                    if resolved:
                        logger.info(f"[Jewelry] Success with {sp}")
                        return _save_result(resolved)
                    else:
                        logger.warning(f"[Jewelry] {sp} returned empty/invalid result")
                except Exception as e:
                    logger.error(f"[Jewelry] {sp} attempt {attempt + 1} failed: {e}")
                    logger.debug(traceback.format_exc())
                    if attempt == 0:
                        time.sleep(5)
                    continue

        logger.error("[Jewelry] All jewelry spaces failed!")
        return None

    return await asyncio.to_thread(_r)


# ---------- save result as PNG ----------

def _save_result(src: str) -> str:
    os.makedirs(os.path.join(config.PHOTOS_DIR, "results"), exist_ok=True)
    dest = os.path.join(config.PHOTOS_DIR, "results", f"result_{uuid.uuid4().hex[:10]}.png")
    # Re-save as PNG for maximum quality
    img = Image.open(src).convert("RGB")
    img.save(dest, format="PNG")
    return dest
