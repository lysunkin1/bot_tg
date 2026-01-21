import requests
from app.config import ADMIN_API, ADMIN_CHAT_ID


def notify_manager_with_actions(text: str, lead_id: int):
    """
    Отправляет сообщение в АДМИН-БОТ с кнопками действий
    """
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "📅 Записать",
                        "callback_data": f"book:{lead_id}"
                    },
                    {
                        "text": "📞 Перезвонить",
                        "callback_data": f"call:{lead_id}"
                    }
                ]
            ]
        }
    }

    requests.post(
        f"{ADMIN_API}/sendMessage",
        json=payload
    )
