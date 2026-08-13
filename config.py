import os

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Задайте переменную окружения TELEGRAM_BOT_TOKEN (токен бота из @BotFather)")
