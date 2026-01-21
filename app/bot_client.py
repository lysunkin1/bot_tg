import requests
from app.config import TELEGRAM_CLIENT_BOT_TOKEN

from app.dialog_manager import DialogManager

dialog_manager = DialogManager()


def send_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_CLIENT_BOT_TOKEN}/sendMessage"
    response = requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    })
    print("Telegram send_message response:", response.text)


async def handle_client_update(update: dict):
    try:
        if "message" not in update:
            return

        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        # /start
        if text == "/start":
            send_message(
                chat_id,
                "Здравствуйте 👋 Подскажите, какая услуга вас интересует?"
            )
            dialog_manager.start(chat_id)
            return

        # обычный текст
        reply = dialog_manager.process_message(chat_id, text)
        if reply:
            send_message(chat_id, reply)

    except Exception as e:
        print("❌ Error in handle_client_update:", e)
