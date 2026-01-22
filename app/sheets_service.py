import requests
from app.config import GOOGLE_SHEETS_WEBHOOK


def send_to_sheets(lead: dict):
    requests.post(
        GOOGLE_SHEETS_WEBHOOK,
        json=lead,
        timeout=5
    )


def update_lead_status(lead_id: int, status: str):
    payload = {
        "action": "update_status",
        "lead_id": lead_id,
        "admin_status": status
    }
    requests.post(
        GOOGLE_SHEETS_WEBHOOK,
        json=payload,
        timeout=5
    )


def update_admin_comment(lead_id: int, comment: str):
    payload = {
        "action": "update_comment",
        "lead_id": lead_id,
        "admin_comment": comment
    }
    requests.post(
        GOOGLE_SHEETS_WEBHOOK,
        json=payload,
        timeout=5
    )
