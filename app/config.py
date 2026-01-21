import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_BOT_TOKEN = os.getenv("CLIENT_BOT_TOKEN")
ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CLIENT_API = f"https://api.telegram.org/bot{CLIENT_BOT_TOKEN}"
ADMIN_API = f"https://api.telegram.org/bot{ADMIN_BOT_TOKEN}"

ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
