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

        # ───── /start — всегда сбрасывает ─────
        if text == "/start":
            self.state[chat_id] = {}
            await self.bot.send_message(
                chat_id,
                "Здравствуйте 👋\nКакую услугу вы хотите?"
            )
            return

        # ───── если диалог не начат ─────
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
            await self.bot.send_message(chat_id, "Как вас зовут?")
            return

        # ───── шаг 2: имя ─────
        if "name" not in data:
            data["name"] = text
            await self.bot.send_message(chat_id, "Введите номер телефона 📞")
            return

        # ───── шаг 3: телефон ─────
        if "phone" not in data:
            data["phone"] = text
            await self.bot.send_message(
                chat_id,
                "Когда вам удобно прийти?\n\n"
                "📅 Пример: 25 января после 16:00"
            )
            return

        # ───── шаг 4: желаемое время ─────
        if "visit_time" not in data:
            data["visit_time"] = text

            # 🤖 AI-анализ
            ai = analyze_lead(data)

            # 📦 ЛИД под Google Sheets
            lead = {
                "created_at": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "lead_id": chat_id,
                "client_name": data["name"],
                "phone": data["phone"],
                "service": data["service"],
                "ai_status": ai["status"],
                "ai_comment": ai["comment"],
                "admin_status": "",
                "admin_comment": f"Желаемое время: {data['visit_time']}",
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
                "Спасибо 🙌\nМы получили вашу заявку и скоро свяжемся с вами."
            )

            # 🧹 очистка состояния
            self.state.pop(chat_id, None)
