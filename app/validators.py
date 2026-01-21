import re
from datetime import datetime, timedelta


def is_valid_phone_ua(phone: str) -> bool:
    digits = re.sub(r"\D", "", phone)

    # +380XXXXXXXXX / 380XXXXXXXXX / 0XXXXXXXXX
    if digits.startswith("380") and len(digits) == 12:
        return True
    if digits.startswith("0") and len(digits) == 10:
        return True

    return False


def normalize_phone_ua(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)

    if digits.startswith("0"):
        return "+38" + digits
    if digits.startswith("380"):
        return "+" + digits

    return phone


def get_date_label(key: str) -> str:
    today = datetime.now().date()

    if key == "today":
        return today.strftime("%d.%m.%Y")

    if key == "tomorrow":
        return (today + timedelta(days=1)).strftime("%d.%m.%Y")

    return ""
