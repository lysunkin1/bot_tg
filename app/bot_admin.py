import requests
from app.config import TELEGRAM_ADMIN_BOT_TOKEN, ADMIN_CHAT_ID
from app.sheets_service import update_lead_status


async def handle_admin_update(update: dict):
    if "callback_query" in update:
        handle_callback(update["callback_query"])
        return


def handle_callback(callback: dict):
    data = callback["data"]
    callback_id = callback["id"]

    if data.startswith("status:"):
        _, status, lead_id = data.split(":")

        update_lead_status(int(lead_id), status)

        answer_callback(
            callback_id,
            f"Статус оновлено: {status}"
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
