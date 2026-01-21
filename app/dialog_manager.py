from datetime import datetime, timedelta

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

        # ─── /start ───
        if text == "/start":
            self.state[chat_id] = {"step": "service"}
            await self.send_services(chat_id)
            return

        if data is None:
            self.state[chat_id] = {"step": "service"}
            await self.send_services(chat_id)
            return

        step = data["step"]

        # ─── УСЛУГА ───
        if step == "service":
            if callback_data and callback_data.startswith("service:"):
                key = callback_data.split(":")[1]
                service = SERVICES[key]
                data["service"] = f"{service['title']} — {service['price']} грн"
                data["step"] = "name"
                await self.bot.send_message(chat_id, "Як вас звати?")
            return

        # ─── ИМЯ ───
        if step == "name":
            data["name"] = text
            data["step"] = "phone"
            await self.bot.send_message(
                chat_id,
                "Введіть номер телефону 📞\nПриклад: +380501234567"
            )
            return

        # ─── ТЕЛЕФОН ───
        if step == "phone":
            if not is_valid_phone_ua(text):
                await self.bot.send_message(
                    chat_id,
                    "❌ Невірний номер.\nФормат: +380501234567 або 0501234567"
                )
                return

            data["phone"] = normalize_phone_ua(text)
            data["step"] = "date"

            keyboard = {
                "inline_keyboard": [
                    [
                        {"text": "Сьогодні", "callback_data": "date:today"},
                        {"text": "Завтра", "callback_data": "date:tomorrow"}
                    ],
                    [
                        {"text": "Ввести дату вручну", "callback_data": "date:manual"}
                    ]
                ]
            }

            await self.bot.send_message(
                chat_id,
                "Оберіть дату візиту 📅",
                reply_markup=keyboard
            )
            return

        # ─── ДАТА (кнопки) ───
        if step == "date" and callback_data:
            today = datetime.now().date()

            if callback_data == "date:today":
                data["visit_date"] = today.strftime("%d.%m.%Y")
                data["step"] = "time"

            elif callback_data == "date:tomorrow":
                data["visit_date"] = (today + timedelta(days=1)).strftime("%d.%m.%Y")
                data["step"] = "time"

            elif callback_data == "date:manual":
                data["step"] = "manual_date"
                await self.bot.send_message(
                    chat_id,
                    "Введіть дату у форматі ДД.ММ.РРРР\nПриклад: 25.01.2026"
                )
                return

            if data["step"] == "time":
                await self.bot.send_message(
                    chat_id,
                    f"Обрана дата: {data['visit_date']}\n"
                    "Напишіть зручний час ⏰"
                )
            return

        # ─── ДАТА (вручну) ───
        if step == "manual_date":
            try:
                date = datetime.strptime(text, "%d.%m.%Y").date()
                if date < datetime.now().date():
                    raise ValueError
            except ValueError:
                await self.bot.send_message(
                    chat_id,
                    "❌ Некоректна дата або дата в минулому.\nСпробуйте ще раз."
                )
                return

            data["visit_date"] = date.strftime("%d.%m.%Y")
            data["step"] = "time"

            await self.bot.send_message(
                chat_id,
                f"Обрана дата: {data['visit_date']}\n"
                "Напишіть зручний час ⏰"
            )
            return

        # ─── ВРЕМЯ ───
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
                "Дякуємо 🙌 Ми звʼяжемось з вами найближчим часом."
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
