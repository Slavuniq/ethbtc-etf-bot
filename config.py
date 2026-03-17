import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN      = os.getenv("BOT_TOKEN","")
ADMIN_IDS      = [int(x) for x in os.getenv("ADMIN_IDS","0").split(",") if x.strip()]
FREE_TRIES     = int(os.getenv("FREE_TRIES","999"))
REFERRAL_BONUS = int(os.getenv("REFERRAL_BONUS","10"))
HF_TOKEN         = os.getenv("HF_TOKEN", None)
HF_TRYON_SPACE   = "yisol/IDM-VTON"
HF_JEWELRY_SPACE = "multimodalart/stable-diffusion-inpainting"
DB_PATH    = "bot_data.db"
PHOTOS_DIR = "photos"
