import requests
from app.config import TELEGRAM_ADMIN_BOT_TOKEN, ADMIN_CHAT_ID

async def handle_admin_update(update: dict):
    if "callback_query" in update:
        handle_callback(update["callback_query"])
        return

    message = update.get("message")
    if not message:
        return

    if message["chat"]["id"] != ADMIN_CHAT_ID:
        return

    if message.get("text") == "/start":
        send_admin_message("👋 Админ-бот готов принимать заявки.")

def handle_callback(callback: dict):
    data = callback["data"]
    callback_id = callback["id"]

    parts = data.split(":")

    if parts[0] == "status":
        _, status, lead_id = parts
        send_admin_message(f"🔥 Лид {lead_id} → {status}")
        answer_callback(callback_id, f"Статус: {status}")

    elif parts[0] == "book":
        lead_id = parts[1]
        send_admin_message(f"📅 Лид {lead_id} записан")
        answer_callback(callback_id, "Записано")

    elif parts[0] == "call":
        lead_id = parts[1]
        send_admin_message(f"📞 Лид {lead_id} — перезвонить")
        answer_callback(callback_id, "Ок")

def send_admin_message(text: str):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_ADMIN_BOT_TOKEN}/sendMessage",
        json={
            "chat_id": ADMIN_CHAT_ID,
            "text": text
        },
        timeout=5
    )

def answer_callback(callback_id: str, text: str):
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_ADMIN_BOT_TOKEN}/answerCallbackQuery",
        json={
            "callback_query_id": callback_id,
            "text": text
        },
        timeout=5
    )
