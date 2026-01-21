from datetime import datetime, timedelta

from app.notifier import notify_admin
from app.crm import save_lead_to_crm
from app.ai_service import analyze_lead


def service_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "💅 Маникюр", "callback_data": "service_Маникюр"}],
            [{"text": "💇‍♀️ Стрижка", "callback_data": "service_Стрижка"}],
            [{"text": "💆‍♀️ Массаж", "callback_data": "service_Массаж"}],
            [{"text": "💄 Макияж", "callback_data": "service_Макияж"}],
        ]
    }


def date_keyboard():
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    return {
        "inline_keyboard": [
            [{"text": f"📅 Сегодня ({today})", "callback_data": f"date_{today}"}],
            [{"text": f"📅 Завтра ({tomorrow})", "callback_data": f"date_{tomorrow}"}],
        ]
    }


def time_keyboard():
    return {
        "inline_keyboard": [
            [{"text": "🕒 16:00", "callback_data": "time_16:00"}],
            [{"text": "🕔 17:00", "callback_data": "time_17:00"}],
            [{"text": "🕖 18:00", "callback_data": "time_18:00"}],
        ]
    }


class DialogManager:
    def __init__(self):
        self.state = {}

    async def handle_start(self, chat_id, send_message):
        self.state[chat_id] = {"step": "service"}
        await send_message(
            chat_id,
            "Здравствуйте 👋\nВыберите услугу:",
            reply_markup=service_keyboard(),
        )

    async def handle_callback(self, chat_id, data, send_message):
        user = self.state.setdefault(chat_id, {})

        if data.startswith("service_"):
            user["service"] = data.replace("service_", "")
            user["step"] = "date"

            await send_message(
                chat_id,
                "Выберите дату:",
                reply_markup=date_keyboard(),
            )

        elif data.startswith("date_"):
            user["date"] = data.replace("date_", "")
            user["step"] = "time"

            await send_message(
                chat_id,
                "Выберите время:",
                reply_markup=time_keyboard(),
            )

        elif data.startswith("time_"):
            user["time"] = data.replace("time_", "")
            user["step"] = "name"

            await send_message(chat_id, "Как вас зовут?")

    async def handle_message(self, chat_id, text, send_message):
        user = self.state.get(chat_id)
        if not user:
            await self.handle_start(chat_id, send_message)
            return

        if user["step"] == "name":
            user["name"] = text
            user["step"] = "phone"
            await send_message(chat_id, "Введите номер телефона 📞")

        elif user["step"] == "phone":
            user["phone"] = text

            # ===== AI анализ =====
            ai_result = await analyze_lead(user)

            # ===== CRM =====
            await save_lead_to_crm(
                chat_id=chat_id,
                user=user,
                ai_result=ai_result,
            )

            # ===== Админу =====
            await notify_admin(
                f"📩 Новая заявка\n\n"
                f"👤 Имя: {user['name']}\n"
                f"📞 Телефон: {user['phone']}\n"
                f"💼 Услуга: {user['service']}\n"
                f"📅 Дата: {user['date']} {user['time']}\n\n"
                f"🔥 Статус: {ai_result['status']}\n"
                f"🤖 Комментарий: {ai_result['comment']}"
            )

            await send_message(
                chat_id,
                "Спасибо! 🙌\nЗаявка передана администратору.",
            )

            self.state.pop(chat_id, None)
