from datetime import datetime

from app.ai_service import analyze_lead
from app.sheets_service import send_to_sheets
from app.notifier import notify_admin


class DialogManager:
    def __init__(self, bot):
        self.bot = bot
        self.state = {}

    async def handle(self, chat_id: int, text: str):
        data = self.state.get(chat_id)

        # ───── /start — всегда сбрасывает диалог ─────
        if text == "/start":
            self.state[chat_id] = {}
            await self.bot.send_message(
                chat_id,
                "Здравствуйте 👋\nКакую услугу вы хотите?"
            )
            return

        # ───── если диалог ещё не начат ─────
        if data is None:
            self.state[chat_id] = {}
            await self.bot.send_message(
                chat_id,
                "Здравствуйте 👋\nКакую услугу вы хотите?"
            )
            return

        # ───── шаг 1: услуга ─────
        if "service" not in data:
            data["service"] = text
            await self.bot.send_message(
                chat_id,
                "Как вас зовут?"
            )
            return

        # ───── шаг 2: имя ─────
        if "name" not in data:
            data["name"] = text
            await self.bot.send_message(
                chat_id,
                "Введите номер телефона 📞"
            )
            return

        # ───── шаг 3: телефон → финал ─────
        if "phone" not in data:
            data["phone"] = text

            # 🔹 AI-анализ
            ai = analyze_lead(data)

            # 🔹 ЛИД — СТРОГО ПОД GOOGLE SHEETS
            lead = {
                "created_at": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "lead_id": chat_id,
                "client_name": data["name"],
                "phone": data["phone"],
                "service": data["service"],
                "ai_status": ai["status"],
                "ai_comment": ai["comment"],
                "admin_status": "",
                "admin_comment": "",
                "source": "telegram",
                "updated_at": ""
            }

            # 1️⃣ Google Sheets
            send_to_sheets(lead)

            # 2️⃣ Админ-бот
            notify_admin(lead)

            # 3️⃣ Ответ клиенту
            await self.bot.send_message(
                chat_id,
                "Спасибо 🙌\nЗаявка отправлена администратору."
            )

            # 🧹 очищаем состояние
            self.state.pop(chat_id, None)
