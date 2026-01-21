import requests

CRM_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbwPqa83BQ1mODcxQbWbTbD5VmsYEWrqY6HB6lbE9HUKznmrhGMcibnR748-EJvq-Gc-Dg/exec"


def save_lead_to_crm(lead_id: int, lead: dict, dialog: str):
    payload = {
        "id": lead_id,
        "service": lead.get("service"),
        "status": lead.get("status"),
        "urgency": lead.get("urgency"),
        "client_type": lead.get("client_type"),
        "contact": lead.get("comment"),
        "dialog": dialog
    }

    requests.post(CRM_WEBHOOK_URL, json=payload, timeout=5)
