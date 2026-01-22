import re
from datetime import datetime


def is_valid_name(name: str) -> bool:
    return len(name.strip()) >= 2 and name.isalpha()


def is_valid_phone_ua(phone: str) -> bool:
    digits = re.sub(r"\D", "", phone)
    return (digits.startswith("380") and len(digits) == 12) or (
        digits.startswith("0") and len(digits) == 10
    )


def normalize_phone_ua(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if digits.startswith("0"):
        return "+38" + digits
    if digits.startswith("380"):
        return "+" + digits
    return phone


def parse_visit_datetime(text: str) -> str | None:
    try:
        dt = datetime.strptime(text, "%d.%m.%Y %H:%M")
        if dt < datetime.now():
            return None
        return dt.strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return None
