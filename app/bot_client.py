from telegram import Bot
from app.config import TELEGRAM_CLIENT_BOT_TOKEN
from app.dialog_manager import DialogManager

bot = Bot(token=TELEGRAM_CLIENT_BOT_TOKEN)
dialog_manager = DialogManager(bot)

async def handle_client_update(update: dict):
    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    await dialog_manager.handle(chat_id, text)
