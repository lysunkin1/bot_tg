def analyze_lead(data: dict) -> dict:
    service = data.get("service", "").lower()

    if service in ["массаж", "маникюр"]:
        return {
            "status": "HOT",
            "comment": "Клиент готов к записи."
        }

    return {
        "status": "WARM",
        "comment": "Нужна консультация."
    }
