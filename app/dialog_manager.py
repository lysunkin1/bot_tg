from app.sheets_service import send_to_sheets
from app.ai_service import analyze_lead


class DialogManager:
    def __init__(self, bot):
        self.bot = bot
        self.state = {}
        self.data = {}

    async def handle_start(self, chat_id: int):
        self.state[chat_id] = "service"
        self.data[chat_id] = {}

        await self.bot.send_message(
            chat_id,
            "Здравствуйте 👋\nВыберите услугу:"
        )

    async def handle_message(self, chat_id: int, text: str):
        step = self.state.get(chat_id)

        if step == "service":
            self.data[chat_id]["service"] = text
            self.state[chat_id] = "name"
            await self.bot.send_message(chat_id, "Как вас зовут?")

        elif step == "name":
            self.data[chat_id]["name"] = text
            self.state[chat_id] = "phone"
            await self.bot.send_message(chat_id, "Введите номер телефона 📞")

        elif step == "phone":
            self.data[chat_id]["phone"] = text

            lead = self.data[chat_id]
            lead["client_id"] = chat_id

            ai = analyze_lead(lead)
            lead["status"] = ai["status"]
            lead["comment"] = ai["comment"]

            send_to_sheets(lead)

            await self.bot.send_message(
                chat_id,
                "Спасибо 🙌\nЗаявка передана администратору."
            )

            self.state.pop(chat_id, None)
            self.data.pop(chat_id, None)
