from app.enums import LeadStatus

def analyze_lead(data: dict) -> dict:
    service = data.get("service", "").lower()
    phone = data.get("phone")

    # если есть телефон и конкретная услуга
    if phone and service in ["брови", "ресницы", "маникюр", "массаж"]:
        return {
            "status": LeadStatus.HOT,
            "comment": "Клиент выбрал услугу и оставил телефон — готов к записи"
        }

    # если есть телефон, но услуга неочевидна
    if phone:
        return {
            "status": LeadStatus.WARM,
            "comment": "Клиент оставил телефон, но требуется консультация"
        }

    # если телефона нет (на будущее)
    return {
        "status": LeadStatus.COLD,
        "comment": "Интерес без контактов, холодный лид"
    }
