import requests
from app.config import GOOGLE_SHEETS_WEBHOOK

def send_to_sheets(lead: dict):
    if not GOOGLE_SHEETS_WEBHOOK:
        return
    requests.post(GOOGLE_SHEETS_WEBHOOK, json=lead, timeout=5)
