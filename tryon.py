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
    "yisol/IDM-VTON",
    "Nymbo/Virtual-Try-On",
    "BestWishYsh/IDM-VTON",
    "kadirnar/IDM-VTON",
]

JEWELRY_SPACES = [
    config.HF_JEWELRY_SPACE,
    "runwayml/stable-diffusion-inpainting",
]

# ---------- space-specific predict functions ----------

def _predict_idm_vton(client, prep_pp, prep_gp):
    """Predict using yisol/IDM-VTON style API (named parameters)."""
    return client.predict(
        dict={"background": handle_file(prep_pp), "layers": [], "composite": None},
        garm_img=handle_file(prep_gp),
        garment_des="a garment, high quality fashion photo",
        is_checked=True,
        is_checked_crop=True,
        denoise_steps=50,
        seed=42,
        api_name="/tryon",
    )


def _predict_nymbo(client, prep_pp, prep_gp):
    """Predict using Nymbo/Virtual-Try-On style API (positional parameters)."""
    return client.predict(
        {"background": handle_file(prep_pp), "layers": [], "composite": None},
        handle_file(prep_gp),
        "auto",     # masking mode
        True,       # use auto mask
        True,       # enhance output
        30,         # denoising steps
        42,         # seed
        api_name="/tryon",
    )


# Mapping: space name → predict function
SPACE_PREDICT = {
    "yisol/IDM-VTON": _predict_idm_vton,
    "Nymbo/Virtual-Try-On": _predict_nymbo,
    "BestWishYsh/IDM-VTON": _predict_idm_vton,
    "kadirnar/IDM-VTON": _predict_idm_vton,
}

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
        for key in ("path", "url", "image", "name", "value"):
            val = res.get(key)
            if val:
                res = val
                break
        else:
            logger.warning(f"[VTON] Dict result has no usable key: {list(res.keys())}")
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
        prep_pp = _prepare_image(pp, 768, 1024)
        prep_gp = _prepare_image(gp, 768, 1024)

        try:
            for sp in CLOTHES_SPACES:
                predict_fn = SPACE_PREDICT.get(sp, _predict_idm_vton)
                for attempt in range(2):
                    try:
                        logger.info(f"[VTON] Trying space: {sp} (attempt {attempt + 1})")
                        c = Client(sp, hf_token=config.HF_TOKEN)
                        res = predict_fn(c, prep_pp, prep_gp)
                        resolved = _resolve_result(res)
                        if resolved:
                            logger.info(f"[VTON] Success with {sp}")
                            return _save_result(resolved)
                        else:
                            logger.warning(f"[VTON] {sp} returned empty/invalid result")
                    except Exception as e:
                        logger.error(f"[VTON] {sp} attempt {attempt + 1} failed: {type(e).__name__}: {e}")
                        logger.debug(traceback.format_exc())
                        if attempt == 0:
                            time.sleep(5)
                        continue

            logger.error("[VTON] All clothes try-on spaces failed!")
            return None
        finally:
            # Clean up temp files
            for f in (prep_pp, prep_gp):
                try:
                    os.unlink(f)
                except OSError:
                    pass

    return await asyncio.to_thread(_r)


# ---------- jewelry try-on ----------

async def run_jewelry_tryon(pp: str, jp: str, jt: str = "necklace"):
    pr = JP.get(jt, f"wearing a {jt}, photorealistic")

    def _r():
        prep_pp = _prepare_image(pp, 512, 512)

        try:
            for sp in JEWELRY_SPACES:
                for attempt in range(2):
                    try:
                        logger.info(f"[Jewelry] Trying space: {sp} (attempt {attempt + 1})")
                        c = Client(sp, hf_token=config.HF_TOKEN)
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
                        logger.error(f"[Jewelry] {sp} attempt {attempt + 1} failed: {type(e).__name__}: {e}")
                        logger.debug(traceback.format_exc())
                        if attempt == 0:
                            time.sleep(5)
                        continue

            logger.error("[Jewelry] All jewelry spaces failed!")
            return None
        finally:
            try:
                os.unlink(prep_pp)
            except OSError:
                pass

    return await asyncio.to_thread(_r)


# ---------- save result as PNG ----------

def _save_result(src: str) -> str:
    os.makedirs(os.path.join(config.PHOTOS_DIR, "results"), exist_ok=True)
    dest = os.path.join(config.PHOTOS_DIR, "results", f"result_{uuid.uuid4().hex[:10]}.png")
    img = Image.open(src).convert("RGB")
    img.save(dest, format="PNG")
    return dest
