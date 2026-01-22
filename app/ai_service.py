from datetime import datetime
import re


RELATIVE_KEYWORDS = [
    "завтра",
    "сьогодні",
    "сегодня",
    "today",
    "tomorrow",
]

FUZZY_KEYWORDS = [
    "після",
    "после",
    "ввечері",
    "вечером",
    "утром",
    "днем",
    "як скажете",
    "як зручно",
]


def analyze_lead(payload: dict) -> dict:
    service = payload.get("service")
    phone = payload.get("phone")
    visit_raw = (payload.get("visit_datetime") or "").lower()

    # ❄️ COLD — нет базы
    if not service or not phone:
        return {
            "ai_status": "COLD",
            "ai_comment": "Недостатньо даних для обробки заявки"
        }

    # 🔍 1. Пытаемся распарсить точную дату
    try:
        visit_dt = datetime.strptime(visit_raw, "%d.%m.%Y %H:%M")
        if visit_dt > datetime.now():
            return {
                "ai_status": "HOT",
                "ai_comment": "Клієнт обрав послугу та конкретний час візиту"
            }
    except Exception:
        pass

    # 🔍 2. Проверяем относительные даты (завтра, сьогодні)
    if any(word in visit_raw for word in RELATIVE_KEYWORDS):
        return {
            "ai_status": "HOT",
            "ai_comment": "Клієнт готовий прийти найближчим часом"
        }

    # 🔍 3. Размытые формулировки
    if any(word in visit_raw for word in FUZZY_KEYWORDS):
        return {
            "ai_status": "WARM",
            "ai_comment": "Потрібно уточнити дату або час візиту"
        }

    # 🟡 fallback — дата есть, но неясная
    if visit_raw:
        return {
            "ai_status": "WARM",
            "ai_comment": "Дата візиту потребує уточнення"
        }

    # ❄️ крайний случай
    return {
        "ai_status": "COLD",
        "ai_comment": "Недостатньо інформації для запису"
    }
