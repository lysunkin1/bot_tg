import httpx
from app.config import TELEGRAM_CLIENT_BOT_TOKEN
from app.dialog_manager import DialogManager

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_CLIENT_BOT_TOKEN}"

dialog_manager = DialogManager()


async def send_message(chat_id: int, text: str, reply_markup: dict | None = None):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
    }

    if reply_markup:
        payload["reply_markup"] = reply_markup

    async with httpx.AsyncClient() as client:
        await client.post(
            f"{TELEGRAM_API_URL}/sendMessage",
            json=payload,
            timeout=10,
        )


async def handle_client_update(update: dict):
    """
    Главная точка входа для webhook клиента
    """

    try:
        # ===== CALLBACK (кнопки) =====
        if "callback_query" in update:
            callback = update["callback_query"]
            chat_id = callback["message"]["chat"]["id"]
            data = callback["data"]

            await dialog_manager.handle_callback(
                chat_id=chat_id,
                data=data,
                send_message=send_message,
            )
            return

        # ===== СООБЩЕНИЯ =====
        if "message" not in update:
            return

        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()

        if not text:
            return

        if text == "/start":
            await dialog_manager.handle_start(
                chat_id=chat_id,
                send_message=send_message,
            )
        else:
            await dialog_manager.handle_message(
                chat_id=chat_id,
                text=text,
                send_message=send_message,
            )

    except Exception as e:
        print("❌ Error in handle_client_update:", e)
