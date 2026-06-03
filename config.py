import os

# Токен бота. Приоритет — переменная окружения (GitHub Secret TELEGRAM_TOKEN),
# чтобы не хранить секрет в коде. Запасное значение оставлено для совместимости.
TOKEN = (
    os.environ.get("TELEGRAM_TOKEN")
    or os.environ.get("TOKEN")
    or "8439594417:AAGGgPPIFf1drF2MSCph60kQ_FG-EB6Kr1E"
)
