import asyncio, logging, os, uuid, tempfile, time, traceback
from PIL import Image
from gradio_client import Client, handle_file
import httpx
import config

logger = logging.getLogger(__name__)

JP = {
    "necklace": "a beautiful elegant necklace, jewelry product photo",
    "earrings": "stylish earrings, jewelry product photo",
    "bracelet": "an elegant bracelet, jewelry product photo",
    "ring": "a beautiful ring, jewelry product photo",
    "watch": "a luxury wristwatch, product photo",
    "glasses": "stylish sunglasses, product photo",
}

# ---------- HF Spaces (порядок = приоритет) ----------

VTON_SPACES = [
    "Nymbo/Virtual-Try-On",      # основной, подтверждённо работает
    "yisol/IDM-VTON",            # оригинальный, часто спит
    "kadirnar/IDM-VTON",         # клон, запасной
]

# ---------- единая predict-функция ----------

def _predict_vton(client, prep_pp, prep_gp, garment_des="a garment"):
    """Вызов /tryon — единый API для всех IDM-VTON и Nymbo Spaces."""
    return client.predict(
        dict={"background": handle_file(prep_pp), "layers": [], "composite": None},
        garm_img=handle_file(prep_gp),
        garment_des=garment_des,
        is_checked=True,
        is_checked_crop=False,
        denoise_steps=30,
        seed=42,
        api_name="/tryon",
    )


# ---------- image preprocessing ----------

def _prepare_image(path: str, target_w: int, target_h: int) -> str:
    """Resize image to target dimensions using LANCZOS, save as PNG temp file."""
    img = Image.open(path).convert("RGB")
    img = img.resize((target_w, target_h), Image.LANCZOS)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name, format="PNG")
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
        with httpx.Client(timeout=60, follow_redirects=True) as hc:
            resp = hc.get(url)
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
            for sp in VTON_SPACES:
                for attempt in range(2):
                    try:
                        logger.info(f"[VTON] Trying space: {sp} (attempt {attempt + 1})")
                        c = Client(sp, hf_token=config.HF_TOKEN)
                        res = _predict_vton(c, prep_pp, prep_gp)
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
            for f in (prep_pp, prep_gp):
                try:
                    os.unlink(f)
                except OSError:
                    pass

    return await asyncio.to_thread(_r)


# ---------- jewelry try-on ----------

async def run_jewelry_tryon(pp: str, jp: str, jt: str = "necklace"):
    """Jewelry try-on: используем тот же VTON Space, передавая фото украшения как garment."""
    garment_des = JP.get(jt, f"a {jt}, product photo")

    def _r():
        prep_pp = _prepare_image(pp, 768, 1024)
        prep_jp = _prepare_image(jp, 768, 1024)

        try:
            for sp in VTON_SPACES:
                for attempt in range(2):
                    try:
                        logger.info(f"[Jewelry] Trying space: {sp} (attempt {attempt + 1})")
                        c = Client(sp, hf_token=config.HF_TOKEN)
                        res = _predict_vton(c, prep_pp, prep_jp, garment_des=garment_des)
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
            for f in (prep_pp, prep_jp):
                try:
                    os.unlink(f)
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
