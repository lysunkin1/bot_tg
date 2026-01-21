import requests
from app.config import GOOGLE_SHEETS_WEBHOOK


def send_to_sheets(lead: dict) -> None:
    """
    Отправляет лид в Google Sheets через Apps Script webhook
    """

    payload = {
        "client_id": lead.get("client_id"),
        "name": lead.get("name"),
        "phone": lead.get("phone"),
        "service": lead.get("service"),
        "date": lead.get("date"),
        "time": lead.get("time"),
        "status": lead.get("status"),
        "comment": lead.get("comment"),
    }

    try:
        requests.post(
            GOOGLE_SHEETS_WEBHOOK,
            json=payload,
            timeout=5
        )
    except Exception as e:
        # Ошибку логируем, но бота не валим
        print("❌ Error sending to Google Sheets:", e)
