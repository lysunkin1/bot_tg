import os
import httpx

from app.dialog_manager import DialogManager

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_CLIENT_BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

dialog_manager = DialogManager()


async def send_message(chat_id: int, text: str):
    """
    Отправка сообщения в Telegram
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
            },
            timeout=10,
        )

        response.raise_for_status()


async def handle_client_update(update: dict):
    """
    Обработка входящего webhook от Telegram
    """
    if "message" not in update:
        return

    chat_id = update["message"]["chat"]["id"]
    text = update["message"].get("text", "")

    if text == "/start":
        await dialog_manager.handle_start(chat_id, send_message)
    else:
        await dialog_manager.handle_message(chat_id, text, send_message)
