import asyncio, logging, os, shutil, uuid, tempfile
from PIL import Image
from gradio_client import Client, handle_file
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

# ---------- image preprocessing ----------

def _prepare_image(path: str, target_w: int, target_h: int) -> str:
    """Resize image to target dimensions using LANCZOS, save as PNG temp file."""
    img = Image.open(path).convert("RGB")
    img = img.resize((target_w, target_h), Image.LANCZOS)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    img.save(tmp.name, format="PNG", quality=100)
    tmp.close()
    return tmp.name


# ---------- clothes try-on ----------

async def run_clothes_tryon(pp: str, gp: str):
    def _r():
        # Prepare images: IDM-VTON expects 768x1024
        prep_pp = _prepare_image(pp, 768, 1024)
        prep_gp = _prepare_image(gp, 768, 1024)

        spaces = [config.HF_TRYON_SPACE, "Nymbo/Virtual-Try-On"]
        for sp in spaces:
            try:
                logger.info(f"[VTON] Trying space: {sp}")
                c = Client(sp)
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
                if isinstance(res, (list, tuple)) and len(res) >= 1:
                    op = res[0]
                    if isinstance(op, dict):
                        op = op.get("path") or op.get("url")
                    if op and os.path.exists(str(op)):
                        logger.info(f"[VTON] Success with {sp}")
                        return _save_result(str(op))
            except Exception as e:
                logger.error(f"[VTON] {sp} failed: {e}")
                continue
        return None

    return await asyncio.to_thread(_r)


# ---------- jewelry try-on ----------

async def run_jewelry_tryon(pp: str, jp: str, jt: str = "necklace"):
    pr = JP.get(jt, f"wearing a {jt}, photorealistic")

    def _r():
        prep_pp = _prepare_image(pp, 512, 512)
        try:
            c = Client(config.HF_JEWELRY_SPACE)
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
            out = res[0] if isinstance(res, (list, tuple)) else res
            if isinstance(out, dict):
                out = out.get("path") or out.get("url") or out.get("image")
            if out and os.path.exists(str(out)):
                return _save_result(str(out))
            return None
        except Exception as e:
            logger.error(f"[Jewelry] {e}")
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
