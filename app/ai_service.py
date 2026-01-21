from app.enums import LeadStatus

def analyze_lead(data: dict) -> dict:
    service = data.get("service", "").lower()

    if service in ["массаж", "маникюр"]:
        return {
            "status": LeadStatus.HOT,
            "comment": "Клиент готов к записи"
        }

    return {
        "status": LeadStatus.WARM,
        "comment": "Нужна консультация"
    }
