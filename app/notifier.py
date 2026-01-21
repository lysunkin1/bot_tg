import requests
from app.config import TELEGRAM_ADMIN_BOT_TOKEN, ADMIN_CHAT_ID


def notify_manager_with_actions(text: str, lead_id: int):
    url = f"https://api.telegram.org/bot{TELEGRAM_ADMIN_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {"text": "📅 Записать", "callback_data": f"book:{lead_id}"},
                    {"text": "📞 Перезвонить", "callback_data": f"call:{lead_id}"}
                ]
            ]
        }
    }

    response = requests.post(url, json=payload)
    print("Admin notify response:", response.text)
