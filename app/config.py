import os

GOOGLE_SHEETS_WEBHOOK = os.getenv("GOOGLE_SHEETS_WEBHOOK")

if not GOOGLE_SHEETS_WEBHOOK:
    raise RuntimeError("GOOGLE_SHEETS_WEBHOOK is not set")
