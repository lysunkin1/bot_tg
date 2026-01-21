import requests
from app.config import TELEGRAM_ADMIN_BOT_TOKEN, ADMIN_CHAT_ID


def notify_admin(lead: dict):
    """
    Отправляет заявку во второй (админский) Telegram-бот
    """

    text = (
        "📩 Новая заявка\n\n"
        f"🆔 ID клиента: {lead['client_id']}\n"
        f"👤 Имя: {lead['name']}\n"
        f"📞 Телефон: {lead['phone']}\n"
        f"💼 Услуга: {lead['service']}\n"
        f"📅 Дата: {lead['date']} {lead['time']}\n\n"
        f"🔥 Статус: {lead['status']}\n"
        f"💬 Комментарий: {lead['comment']}"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_ADMIN_BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": ADMIN_CHAT_ID,
            "text": text
        },
        timeout=5
    )