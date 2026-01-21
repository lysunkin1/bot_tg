import os

# =========================
# Telegram bots
# =========================

# Клиентский бот (тот, где выбирают услуги)
TELEGRAM_CLIENT_BOT_TOKEN = os.getenv("TELEGRAM_CLIENT_BOT_TOKEN")
if not TELEGRAM_CLIENT_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_CLIENT_BOT_TOKEN is not set")

# Админ-бот (куда приходят заявки)
TELEGRAM_ADMIN_BOT_TOKEN = os.getenv("TELEGRAM_ADMIN_BOT_TOKEN")
if not TELEGRAM_ADMIN_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_ADMIN_BOT_TOKEN is not set")

# ID чата администратора (число!)
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
if not ADMIN_CHAT_ID:
    raise RuntimeError("ADMIN_CHAT_ID is not set")

ADMIN_CHAT_ID = int(ADMIN_CHAT_ID)

# =========================
# Webhooks
# =========================

# Webhook путь для клиентского бота
CLIENT_WEBHOOK_PATH = "/webhook/client"

# Webhook путь для админ-бота
ADMIN_WEBHOOK_PATH = "/webhook/admin"

# =========================
# Google Sheets
# =========================

# URL Google Apps Script (Web App)
GOOGLE_SHEETS_WEBHOOK = os.getenv("GOOGLE_SHEETS_WEBHOOK")
if not GOOGLE_SHEETS_WEBHOOK:
    raise RuntimeError("GOOGLE_SHEETS_WEBHOOK is not set")

# =========================
# OpenAI
# =========================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")

# =========================
# Services & buttons
# =========================

SERVICES = [
    "Маникюр",
    "Стрижка",
    "Массаж",
    "Макияж",
]

# Даты (генерируются логикой, но подписи здесь)
DATE_TODAY_LABEL = "Сегодня"
DATE_TOMORROW_LABEL = "Завтра"

# Время записи
TIME_SLOTS = [
    "16:00",
    "17:00",
    "18:00",
]

# =========================
# Lead statuses
# =========================

LEAD_STATUS_HOT = "HOT"
LEAD_STATUS_WARM = "WARM"
LEAD_STATUS_COLD = "COLD"
