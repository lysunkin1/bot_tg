from datetime import datetime

from app.ai_service import analyze_lead
from app.sheets_service import send_to_sheets
from app.notifier import notify_admin
from app.validators import is_valid_phone_ua, normalize_phone_ua
from app.services import SERVICES


class DialogManager:
    def __init__(self, bot):
        self.bot = bot
        self.state = {}

    async def handle(self, chat_id: int, text: str = "", callback_data: str | None = None):
        data = self.state.get(chat_id)

        # /start
        if text == "/start":
            self.state[chat_id] = {"step": "service"}
            await self.send_services(chat_id)
            return

        if data is None:
            self.state[chat_id] = {"step": "service"}
            await self.send_services(chat_id)
            return

        step = data.get("step")

        # ───── УСЛУГА ─────
        if step == "service":
            if callback_data and callback_data.startswith("service:"):
                key = callback_data.split(":")[1]
                service = SERVICES[key]

                data["service"] = f"{service['title']} — {service['price']} грн"
                data["step"] = "name"

                await self.bot.send_message(chat_id, "Як вас звати?")
            return

        # ───── ИМЯ ─────
        if step == "name":
            data["name"] = text
            data["step"] = "phone"
            await self.bot.send_message(
                chat_id,
                "Введіть номер телефону 📞\nПриклад: +380501234567"
            )
            return

        # ───── ТЕЛЕФОН ─────
        if step == "phone":
            if not is_valid_phone_ua(text):
                await self.bot.send_message(
                    chat_id,
                    "❌ Невірний формат номера.\nСпробуйте ще раз."
                )
                return

            data["phone"] = normalize_phone_ua(text)
            data["step"] = "date"

            keyboard = {
                "inline_keyboard": [
                    [
                        {"text": "Сьогодні", "callback_data": "date:today"},
                        {"text": "Завтра", "callback_data": "date:tomorrow"}
                    ]
                ]
            }

            await self.bot.send_message(
                chat_id,
                "Оберіть дату візиту 📅",
                reply_markup=keyboard
            )
            return

        # ───── ДАТА ─────
        if step == "date" and callback_data:
            if callback_data.startswith("date:"):
                key = callback_data.split(":")[1]
                today = datetime.now().date()

                if key == "today":
                    data["visit_date"] = today.strftime("%d.%m.%Y")
                elif key == "tomorrow":
                    data["visit_date"] = (today.replace(day=today.day + 1)).strftime("%d.%m.%Y")

                data["step"] = "time"

                await self.bot.send_message(
                    chat_id,
                    f"Обрана дата: {data['visit_date']}\n"
                    "Напишіть зручний час ⏰\n"
                    "Приклад: 15:30 або після 18:00"
                )
            return

        # ───── ВРЕМЯ ─────
        if step == "time":
            data["visit_time"] = text

            ai = analyze_lead(data)

            lead = {
                "created_at": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "lead_id": chat_id,
                "client_name": data["name"],
                "phone": data["phone"],
                "service": data["service"],
                "ai_status": ai["status"],
                "ai_comment": ai["comment"],
                "admin_status": "",
                "admin_comment": f"{data['visit_date']} {data['visit_time']}",
                "source": "telegram",
                "updated_at": ""
            }

            send_to_sheets(lead)
            notify_admin(lead)

            await self.bot.send_message(
                chat_id,
                "Дякуємо 🙌\nМи отримали вашу заявку та скоро звʼяжемось з вами."
            )

            self.state.pop(chat_id, None)

    async def send_services(self, chat_id: int):
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": f"{s['title']} — {s['price']} грн",
                        "callback_data": f"service:{key}"
                    }
                ]
                for key, s in SERVICES.items()
            ]
        }

        await self.bot.send_message(
            chat_id,
            "Оберіть послугу 💅",
            reply_markup=keyboard
        )
