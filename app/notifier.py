import requests
from app.config import TELEGRAM_ADMIN_BOT_TOKEN, ADMIN_CHAT_ID


def notify_admin(lead: dict):
    text = (
        "📥 Нова заявка\n\n"
        f"👤 Імʼя: {lead['client_name']}\n"
        f"📞 Телефон: {lead['phone']}\n"
        f"💅 Послуга: {lead['service']}\n"
        f"🕒 Час: {lead['admin_comment']}\n"
        f"🤖 AI: {lead['ai_status']}"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "⚙️ Меню", "callback_data": f"menu:{lead['lead_id']}"}
            ]
        ]
    }

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_ADMIN_BOT_TOKEN}/sendMessage",
        json={
            "chat_id": ADMIN_CHAT_ID,
            "text": text,
            "reply_markup": keyboard
        },
        timeout=5
    )
