import requests
from app.config import ADMIN_API, ADMIN_CHAT_ID


async def handle_admin_update(update: dict):
    if "callback_query" in update:
        handle_callback(update["callback_query"])
        return

    if "message" not in update:
        return

    message = update["message"]
    chat_id = message["chat"]["id"]

    if chat_id != ADMIN_CHAT_ID:
        return

    text = message.get("text", "")

    if text == "/start":
        send_admin_message("👋 Админ-бот готов принимать заявки.")


def handle_callback(callback: dict):
    data = callback["data"]
    callback_id = callback["id"]

    if data.startswith("book:"):
        lead_id = data.split(":")[1]
        send_admin_message(f"📅 Лид {lead_id} отмечен как ЗАПИСАННЫЙ")
        answer_callback(callback_id, "Записано")

    elif data.startswith("call:"):
        lead_id = data.split(":")[1]
        send_admin_message(f"📞 Лид {lead_id} отмечен для звонка")
        answer_callback(callback_id, "Отмечено")


def send_admin_message(text: str, buttons: dict | None = None):
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text
    }

    if buttons:
        payload["reply_markup"] = buttons

    requests.post(f"{ADMIN_API}/sendMessage", json=payload)


def answer_callback(callback_id: str, text: str):
    requests.post(
        f"{ADMIN_API}/answerCallbackQuery",
        json={
            "callback_query_id": callback_id,
            "text": text
        }
    )
