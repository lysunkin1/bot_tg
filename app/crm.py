import httpx
import os

CRM_URL = os.getenv("CRM_WEBHOOK_URL")


async def save_lead_to_crm(chat_id, user, ai_text):
    async with httpx.AsyncClient() as client:
        await client.post(
            CRM_URL,
            json={
                "chat_id": chat_id,
                "name": user["name"],
                "phone": user["phone"],
                "service": user["service"],
                "ai": ai_text,
            },
            timeout=10,
        )
