"""
Configuration for Polina Manokhina's Telegram Launch Bot.

All secrets are loaded from environment variables.
Set them in a .env file or export them in your shell before running.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env from the same directory as this file (or project root)
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
load_dotenv(_HERE / ".env")
load_dotenv(_HERE.parent.parent / ".env")  # fallback to repo root

# ---------------------------------------------------------------------------
# Telegram
# ---------------------------------------------------------------------------
BOT_TOKEN: str = os.getenv("MANOKHINA_BOT_TOKEN", "")
ADMIN_IDS: list[int] = [
    int(x.strip())
    for x in os.getenv("MANOKHINA_ADMIN_IDS", "").split(",")
    if x.strip().isdigit()
]

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DB_PATH: str = os.getenv(
    "MANOKHINA_DB_PATH",
    str(_HERE / "bot_database.sqlite3"),
)

# ---------------------------------------------------------------------------
# Product links & prices
# ---------------------------------------------------------------------------
LEAD_MAGNET_URL: str = os.getenv(
    "LEAD_MAGNET_URL",
    "https://manokhina.ai/free-guide",
)

PROMPT_VAULT_URL: str = os.getenv(
    "PROMPT_VAULT_URL",
    "https://manokhina.ai/prompt-vault",
)
PROMPT_VAULT_PRICE: str = "$37"

COURSE_URL: str = os.getenv(
    "COURSE_URL",
    "https://manokhina.ai/cinema-ai-academy",
)
COURSE_PRICE: str = "$497"

WEBINAR_URL: str = os.getenv(
    "WEBINAR_URL",
    "https://manokhina.ai/webinar",
)

# ---------------------------------------------------------------------------
# Webinar schedule  (ISO-8601, UTC)
# ---------------------------------------------------------------------------
WEBINAR_DATETIME: str = os.getenv("WEBINAR_DATETIME", "2026-04-20T18:00:00+00:00")

# ---------------------------------------------------------------------------
# Drip sequence intervals (seconds)
# ---------------------------------------------------------------------------
DRIP_INTERVALS: list[int] = [
    24 * 3600,   # message 1 — 24 h after /start
    48 * 3600,   # message 2 — 48 h
    72 * 3600,   # message 3 — 72 h
    96 * 3600,   # message 4 — 96 h
]

# ---------------------------------------------------------------------------
# Referral bonuses
# ---------------------------------------------------------------------------
REFERRAL_BONUS_THRESHOLD: int = 3  # invites needed to unlock bonus prompts
BONUS_PROMPTS_URL: str = os.getenv(
    "BONUS_PROMPTS_URL",
    "https://manokhina.ai/bonus-prompts",
)
