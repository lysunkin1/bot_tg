# app/dialog_manager.py

from app.notifier import notify_admin
from app.sheets_service import send_to_sheets
from app.ai_service import analyze_lead


class DialogManager:
    def init(self):
        self.states = {}

    async def handle_start(self, chat_id: int, send_message):
        self.states[chat_id] = {}
        await send_message(chat_id, "Здравствуйте 👋\nВыберите услугу:")

    async def handle_message(self, chat_id: int, text: str, send_message):
        state = self.states.get(chat_id, {})

        # Простейший пример логики
        if "service" not in state:
            state["service"] = text
            self.states[chat_id] = state
            await send_message(chat_id, "Введите ваше имя:")
            return

        if "name" not in state:
            state["name"] = text
            self.states[chat_id] = state
            await send_message(chat_id, "Введите номер телефона:")
            return

        if "phone" not in state:
            state["phone"] = text

            lead = {
                "name": state["name"],
                "phone": state["phone"],
                "service": state["service"],
            }

            # AI анализ
            ai_result = analyze_lead(lead)
            lead.update(ai_result)

            # Google Sheets
            send_to_sheets(lead)

            # Админ-бот
            await notify_admin(lead)

            await send_message(chat_id, "Спасибо! 🙌 Заявка принята.")
            self.states.pop(chat_id, None)