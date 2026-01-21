import os

# Клиентский бот
TELEGRAM_CLIENT_BOT_TOKEN = os.getenv("TELEGRAM_CLIENT_BOT_TOKEN")

# Админский бот
TELEGRAM_ADMIN_BOT_TOKEN = os.getenv("TELEGRAM_ADMIN_BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

# Google Sheets
GOOGLE_SHEETS_WEBHOOK = os.getenv("GOOGLE_SHEETS_WEBHOOK")

if not TELEGRAM_CLIENT_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_CLIENT_BOT_TOKEN not set")

if not TELEGRAM_ADMIN_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_ADMIN_BOT_TOKEN not set")

if not ADMIN_CHAT_ID:
    raise RuntimeError("ADMIN_CHAT_ID not set")

if not GOOGLE_SHEETS_WEBHOOK:
    raise RuntimeError("GOOGLE_SHEETS_WEBHOOK not set")
