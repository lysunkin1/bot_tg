from app.ai_service import analyze_lead
from app.sheets_service import send_to_sheets
from app.notifier import notify_admin

class DialogManager:
    def __init__(self, bot):
        self.bot = bot
        self.state = {}

    async def handle(self, chat_id: int, text: str):
        data = self.state.get(chat_id)

        # /start — сброс
        if text == "/start":
            self.state[chat_id] = {}
            await self.bot.send_message(
                chat_id,
                "Здравствуйте 👋\nКакую услугу вы хотите?"
            )
            return

        # если диалог не начат
        if data is None:
            self.state[chat_id] = {}
            await self.bot.send_message(
                chat_id,
                "Здравствуйте 👋\nКакую услугу вы хотите?"
            )
            return

        # услуга
        if "service" not in data:
            data["service"] = text
            await self.bot.send_message(chat_id, "Как вас зовут?")
            return

        # имя
        if "name" not in data:
            data["name"] = text
            await self.bot.send_message(chat_id, "Введите номер телефона 📞")
            return

        # телефон → финал
        if "phone" not in data:
            data["phone"] = text

            ai = analyze_lead(data)

            lead = {
                "client_id": chat_id,
                "service": data["service"],
                "name": data["name"],
                "phone": data["phone"],
                "date": "не указана",
                "time": "не указано",
                "status": ai["status"],
                "comment": ai["comment"]
            }

            send_to_sheets(lead)
            notify_admin(lead)

            await self.bot.send_message(
                chat_id,
                "Спасибо 🙌\nЗаявка отправлена администратору."
            )

            self.state.pop(chat_id, None)
