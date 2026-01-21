import requests
from app.config import TELEGRAM_ADMIN_BOT_TOKEN, ADMIN_CHAT_ID
from app.sheets_service import update_lead_status, update_admin_comment
from app.admin_state import admin_state


async def handle_admin_update(update: dict):
    if "callback_query" in update:
        handle_callback(update["callback_query"])
        return

    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if chat_id != ADMIN_CHAT_ID:
        return

    state = admin_state.get(chat_id)
    if state and state["step"] == "await_comment":
        update_admin_comment(state["lead_id"], text)
        admin_state.pop(chat_id)
        send_admin_message("✅ Коментар збережено")


def handle_callback(callback: dict):
    data = callback["data"]
    callback_id = callback["id"]

    if data.startswith("menu:"):
        lead_id = int(data.split(":")[1])
        send_menu(lead_id)
        answer_callback(callback_id, "Меню")
        return

    if data.startswith("status:"):
        _, status, lead_id = data.split(":")
        update_lead_status(int(lead_id), status)
        answer_callback(callback_id, f"Статус: {status}")
        return

    if data.startswith("comment:"):
        lead_id = int(data.split(":")[1])
        admin_state[ADMIN_CHAT_ID] = {
            "step": "await_comment",
            "lead_id": lead_id
        }
        send_admin_message("✏️ Напишіть коментар для цього ліда")
        answer_callback(callback_id, "Очікую коментар")


def send_menu(lead_id: int):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔥 HOT", "callback_data": f"status:HOT:{lead_id}"},
                {"text": "🟡 WARM", "callback_data": f"status:WARM:{lead_id}"},
                {"text": "❄️ COLD", "callback_data": f"status:COLD:{lead_id}"}
            ],
            [
                {"text": "✏️ Коментар", "callback_data": f"comment:{lead_id}"}
            ]
        ]
    }

    send_admin_message(f"Меню для ліда {lead_id}", keyboard)


def send_admin_message(text: str, keyboard: dict | None = None):
    payload = {"chat_id": ADMIN_CHAT_ID, "text": text}
    if keyboard:
        payload["reply_markup"] = keyboard

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_ADMIN_BOT_TOKEN}/sendMessage",
        json=payload,
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
