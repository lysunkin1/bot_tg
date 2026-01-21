# app/bot_client.py

from telegram import Bot
from app.config import TELEGRAM_CLIENT_BOT_TOKEN
from app.dialog_manager import DialogManager

bot = Bot(token=TELEGRAM_CLIENT_BOT_TOKEN)
dialog_manager = DialogManager()


async def send_message(chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=text)


async def handle_client_update(update: dict):
    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        await dialog_manager.handle_start(chat_id, send_message)
    else:
        await dialog_manager.handle_message(chat_id, text, send_message)