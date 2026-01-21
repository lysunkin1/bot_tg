import os

# Telegram bots
TELEGRAM_CLIENT_BOT_TOKEN = os.getenv("TELEGRAM_CLIENT_BOT_TOKEN")
TELEGRAM_ADMIN_BOT_TOKEN = os.getenv("TELEGRAM_ADMIN_BOT_TOKEN")

# Admin chat
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ---- validation (чтобы падало сразу, а не молча) ----
if not TELEGRAM_CLIENT_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_CLIENT_BOT_TOKEN is not set")

if not TELEGRAM_ADMIN_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_ADMIN_BOT_TOKEN is not set")

if not ADMIN_CHAT_ID:
    raise RuntimeError("ADMIN_CHAT_ID is not set")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not set")
