import requests
from app.dialog_manager import DialogManager
from app.config import CLIENT_API

dialog_manager = DialogManager()


async def handle_client_update(update: dict):
    if "message" not in update:
        return

    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text")

    if not text:
        return

    reply = dialog_manager.handle_message(chat_id, text)

    requests.post(
        f"{CLIENT_API}/sendMessage",
        json={"chat_id": chat_id, "text": reply}
    )
