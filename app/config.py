import os

# =========================
# TELEGRAM
# =========================

TELEGRAM_CLIENT_BOT_TOKEN = os.getenv("TELEGRAM_CLIENT_BOT_TOKEN")
TELEGRAM_ADMIN_BOT_TOKEN = os.getenv("TELEGRAM_ADMIN_BOT_TOKEN")

ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# =========================
# AI
# =========================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# =========================
# GOOGLE SHEETS
# =========================

GOOGLE_SHEETS_WEBHOOK = os.getenv("GOOGLE_SHEETS_WEBHOOK")


# =========================
# VALIDATION (ВАЖНО)
# =========================

missing = []

if not TELEGRAM_CLIENT_BOT_TOKEN:
    missing.append("TELEGRAM_CLIENT_BOT_TOKEN")

if not TELEGRAM_ADMIN_BOT_TOKEN:
    missing.append("TELEGRAM_ADMIN_BOT_TOKEN")

if not ADMIN_CHAT_ID:
    missing.append("ADMIN_CHAT_ID")

if not OPENAI_API_KEY:
    missing.append("OPENAI_API_KEY")

if not GOOGLE_SHEETS_WEBHOOK:
    missing.append("GOOGLE_SHEETS_WEBHOOK")

if missing:
    raise RuntimeError(
        "Missing environment variables: " + ", ".join(missing)
    )
