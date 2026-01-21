from app.sheets_service import send_to_sheets
from app.notifier import notify_admin


class DialogManager:
    def init(self, bot):
        self.bot = bot
        self.state = {}

    async def handle(self, chat_id: int, text: str):
        data = self.state.get(chat_id)

        # START
        if text == "/start" or not data:
            self.state[chat_id] = {}
            await self.bot.send_message(
                chat_id,
                "Здравствуйте 👋\nКакую услугу вы хотите?"
            )
            return

        # Услуга
        if "service" not in data:
            data["service"] = text
            self.state[chat_id] = data
            await self.bot.send_message(chat_id, "Как вас зовут?")
            return

        # Имя
        if "name" not in data:
            data["name"] = text
            await self.bot.send_message(chat_id, "Введите номер телефона 📞")
            return

        # Телефон → финал
        if "phone" not in data:
            data["phone"] = text

            lead = {
                "client_id": chat_id,
                "service": data["service"],
                "name": data["name"],
                "phone": data["phone"],
                "date": "не указана",
                "time": "не указано",
                "status": "NEW",
                "comment": "Новая заявка, требуется обработка"
            }

            # 1️⃣ Google Sheets
            send_to_sheets(lead)

            # 2️⃣ Админский бот
            notify_admin(lead)

            # 3️⃣ Ответ клиенту
            await self.bot.send_message(
                chat_id,
                "Спасибо! 🙌\nЗаявка отправлена администратору."
            )

            # Чистим состояние
            self.state.pop(chat_id, None)