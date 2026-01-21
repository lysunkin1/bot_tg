import os
import httpx

CRM_WEBHOOK_URL = os.getenv("CRM_WEBHOOK_URL")


async def save_lead_to_crm(chat_id: int, user: dict, ai_result: dict):
    payload = {
        "chat_id": chat_id,
        "name": user["name"],
        "phone": user["phone"],
        "service": user["service"],
        "date": user["date"],
        "time": user["time"],
        "status": ai_result["status"],
        "comment": ai_result["comment"],
    }

    async with httpx.AsyncClient() as client:
        await client.post(CRM_WEBHOOK_URL, json=payload, timeout=10)
