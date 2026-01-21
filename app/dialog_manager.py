from telegram import ReplyKeyboardMarkup
from app.ai_service import analyze_lead
from app.sheets_service import send_to_sheets
from app.notifier import notify_admin

class DialogManager:
    def __init__(self, bot):
        self.bot = bot
        self.state = {}

    async def handle(self, chat_id: int, text: str):
        data = self.state.get(chat_id, {})

        if text == "/start":
            self.state[chat_id] = {}
            await self.bot.send_message(
                chat_id,
                "Здравствуйте 👋\nВыберите услугу:",
                reply_markup=ReplyKeyboardMarkup(
                    [["Маникюр", "Стрижка"], ["Массаж", "Макияж"]],
                    resize_keyboard=True
                )
            )
            return

        if "service" not in data:
            data["service"] = text
            self.state[chat_id] = data
            await self.bot.send_message(chat_id, "Введите ваше имя:")
            return

        if "name" not in data:
            data["name"] = text
            await self.bot.send_message(chat_id, "Введите телефон 📞")
            return

        if "phone" not in data:
            data["phone"] = text

            ai = analyze_lead(data)
            lead = {**data, **ai, "chat_id": chat_id}

            send_to_sheets(lead)
            await notify_admin(self.bot, lead)

            await self.bot.send_message(chat_id, "Спасибо! Заявка отправлена 🙌")
            self.state.pop(chat_id, None)
