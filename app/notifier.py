import requests
from app.config import TELEGRAM_ADMIN_BOT_TOKEN, ADMIN_CHAT_ID


def notify_admin(lead: dict):
    text = (
        "📥 Нова заявка\n\n"
        f"🆔 ID: {lead['lead_id']}\n"
        f"👤 Імʼя: {lead['client_name']}\n"
        f"📞 Телефон: {lead['phone']}\n"
        f"💅 Послуга: {lead['service']}\n"
        f"🕒 Час: {lead['visit_datetime']}\n\n"
        f"🤖 AI статус: {lead['ai_status']}\n"
        f"💬 AI коментар: {lead['ai_comment']}"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔥 HOT", "callback_data": f"status:HOT:{lead['lead_id']}"},
                {"text": "🟡 WARM", "callback_data": f"status:WARM:{lead['lead_id']}"},
                {"text": "❄️ COLD", "callback_data": f"status:COLD:{lead['lead_id']}"},
            ],
            [
                {"text": "✏️ Коментар", "callback_data": f"comment:{lead['lead_id']}"}
            ],
        ]
    }

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_ADMIN_BOT_TOKEN}/sendMessage",
        json={"chat_id": ADMIN_CHAT_ID, "text": text, "reply_markup": keyboard},
        timeout=5,
    )
