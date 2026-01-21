import os
import httpx

ADMIN_BOT_TOKEN = os.getenv("TELEGRAM_ADMIN_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

ADMIN_API_URL = f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}"


async def notify_admin(text: str):
    """
    Отправка заявки администратору
    """
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{ADMIN_API_URL}/sendMessage",
            json={
                "chat_id": ADMIN_CHAT_ID,
                "text": text,
                "reply_markup": {
                    "inline_keyboard": [
                        [
                            {"text": "📅 Записать", "callback_data": "admin_book"},
                            {"text": "📞 Перезвонить", "callback_data": "admin_call"},
                        ],
                        [
                            {"text": "❌ Отказ", "callback_data": "admin_reject"},
                        ],
                    ]
                },
            },
            timeout=10,
        )
