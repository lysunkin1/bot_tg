import requests
from app.config import TELEGRAM_ADMIN_BOT_TOKEN, ADMIN_CHAT_ID


def notify_admin(lead: dict):
    text = (
        "📥 *Новая заявка*\n\n"
        f"🆔 ID: {lead['lead_id']}\n"
        f"👤 Имя: {lead['client_name']}\n"
        f"📞 Телефон: {lead['phone']}\n"
        f"💅 Услуга: {lead['service']}\n"
        f"🕒 Желаемое время: {lead.get('admin_comment', '—')}\n"
        f"🤖 AI статус: {lead['ai_status']}\n"
        f"💬 AI комментарий: {lead['ai_comment']}"
    )

    keyboard = {
        "inline_keyboard": [
            [
                {"text": "🔥 HOT", "callback_data": f"status:HOT:{lead['lead_id']}"},
                {"text": "🟡 WARM", "callback_data": f"status:WARM:{lead['lead_id']}"},
                {"text": "❄️ COLD", "callback_data": f"status:COLD:{lead['lead_id']}"}
            ],
            [
                {"text": "📅 Записан", "callback_data": f"book:{lead['lead_id']}"},
                {"text": "📞 Перезвонить", "callback_data": f"call:{lead['lead_id']}"}
            ]
        ]
    }

    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_ADMIN_BOT_TOKEN}/sendMessage",
        json={
            "chat_id": ADMIN_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown",
            "reply_markup": keyboard
        },
        timeout=5
    )
