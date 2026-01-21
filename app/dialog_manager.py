from app.notifier import notify_admin
from app.crm import save_lead_to_crm
from app.ai_service import analyze_lead


class DialogManager:
    def __init__(self):
        self.state = {}

    async def handle_start(self, chat_id, send_message):
        self.state[chat_id] = {"step": "service"}

        await send_message(
            chat_id,
            "Здравствуйте 👋\nВыберите услугу:",
            reply_markup={
                "inline_keyboard": [
                    [{"text": "💅 Маникюр", "callback_data": "service_manicure"}],
                    [{"text": "💇‍♀️ Стрижка", "callback_data": "service_haircut"}],
                    [{"text": "💆‍♀️ Массаж", "callback_data": "service_massage"}],
                    [{"text": "💄 Макияж", "callback_data": "service_makeup"}],
                ]
            },
        )

    async def handle_callback(self, chat_id, data, send_message):
        if data.startswith("service_"):
            service = data.replace("service_", "")
            self.state[chat_id]["service"] = service
            self.state[chat_id]["step"] = "name"

            await send_message(chat_id, "Как вас зовут?")

    async def handle_message(self, chat_id, text, send_message):
        user = self.state.setdefault(chat_id, {})
        step = user.get("step")

        if step == "name":
            user["name"] = text
            user["step"] = "phone"
            await send_message(chat_id, "Введите номер телефона 📞")

        elif step == "phone":
            user["phone"] = text
            user["step"] = "done"

            await send_message(chat_id, "Спасибо! Заявка отправлена администратору 🙌")

            lead_text = (
                f"📩 Новая заявка\n\n"
                f"👤 Имя: {user['name']}\n"
                f"📞 Телефон: {user['phone']}\n"
                f"💼 Услуга: {user['service']}\n"
                f"🆔 Chat ID: {chat_id}"
            )

            # ИИ-анализ
            ai_summary = await analyze_lead(user)

            await notify_admin(lead_text + "\n\n🤖 ИИ:\n" + ai_summary)
            await save_lead_to_crm(chat_id, user, ai_summary)
