def analyze_lead(payload: dict) -> dict:
    """
    payload:
    - service
    - phone
    - visit_datetime
    """

    service = payload.get("service")
    phone = payload.get("phone")
    visit = payload.get("visit_datetime")

    if service and phone and visit:
        return {
            "ai_status": "HOT",
            "ai_comment": "Клієнт обрав послугу, залишив номер та час візиту"
        }

    if service and phone:
        return {
            "ai_status": "WARM",
            "ai_comment": "Клієнт зацікавлений, потрібно уточнити час"
        }

    return {
        "ai_status": "COLD",
        "ai_comment": "Недостатньо даних для запису"
    }
