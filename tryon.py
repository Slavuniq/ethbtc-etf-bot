import asyncio
import logging
import os
import shutil
import uuid

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


async def run_clothes_tryon(pp, gp):
    def _r():
        try:
            c = Client(config.HF_TRYON_SPACE)
            res = c.predict(
                dict={
                    "background": handle_file(pp),
                    "layers": [],
                    "composite": None,
                },
                garm_img=handle_file(gp),
                garment_des="clothing item",
                is_checked=True,
                is_checked_crop=False,
                denoise_steps=30,
                seed=42,
                api_name="/tryon",
            )
            if isinstance(res, (list, tuple)) and len(res) >= 1:
                op = res[0]
                if isinstance(op, dict):
                    op = op.get("path") or op.get("url")
                if op and os.path.exists(str(op)):
                    return _cp(str(op))
            return None
        except Exception as e:
            logger.error(f"[VTON] {e}")
            return None

    return await asyncio.to_thread(_r)


async def run_jewelry_tryon(pp, jp, jt="necklace"):
    pr = JP.get(jt, f"wearing a {jt}, photorealistic")

    def _r():
        try:
            c = Client(config.HF_JEWELRY_SPACE)
            res = c.predict(
                prompt=pr,
                negative_prompt="blurry,deformed,ugly",
                image=handle_file(pp),
                mask_image=handle_file(pp),
                steps=25,
                guidance_scale=7.5,
                strength=0.4,
                api_name="/infer",
            )
            out = res[0] if isinstance(res, (list, tuple)) else res
            if isinstance(out, dict):
                out = out.get("path") or out.get("url") or out.get("image")
            if out and os.path.exists(str(out)):
                return _cp(str(out))
            return None
        except Exception as e:
            logger.error(f"[Jewelry] {e}")
            return None

    return await asyncio.to_thread(_r)


def _cp(src):
    os.makedirs(os.path.join(config.PHOTOS_DIR, "results"), exist_ok=True)
    ext = os.path.splitext(src)[1] or ".jpg"
    dest = os.path.join(
        config.PHOTOS_DIR, "results", f"result_{uuid.uuid4().hex[:10]}{ext}"
    )
    shutil.copy2(src, dest)
    return dest
