from datetime import datetime

from app.ai_service import analyze_lead
from app.sheets_service import send_to_sheets
from app.notifier import notify_admin
from app.validators import (
    is_valid_phone_ua,
    normalize_phone_ua,
    get_date_label,
)


class DialogManager:
    def __init__(self, bot):
        self.bot = bot
        self.state = {}

    async def handle(self, chat_id: int, text: str, callback_data: str | None = None):
        data = self.state.get(chat_id)

        # ───── /start ─────
        if text == "/start":
            self.state[chat_id] = {}
            await self.bot.send_message(
                chat_id,
                "Вітаємо 👋\nЯку послугу ви хочете?"
            )
            return

        # ───── начало ─────
        if data is None:
            self.state[chat_id] = {}
            await self.bot.send_message(
                chat_id,
                "Вітаємо 👋\nЯку послугу ви хочете?"
            )
            return

        # ───── услуга ─────
        if "service" not in data:
            data["service"] = text
            await self.bot.send_message(chat_id, "Як вас звати?")
            return

        # ───── имя ─────
        if "name" not in data:
            data["name"] = text
            await self.bot.send_message(
                chat_id,
                "Введіть номер телефону 📞\n\n"
                "Приклад: +380501234567\n"
                "Ми використовуємо номер лише для звʼязку"
            )
            return

        # ───── телефон ─────
        if "phone" not in data:
            if not is_valid_phone_ua(text):
                await self.bot.send_message(
                    chat_id,
                    "❌ Номер виглядає некоректно.\n"
                    "Введіть номер у форматі:\n"
                    "+380501234567 або 0501234567"
                )
                return

            data["phone"] = normalize_phone_ua(text)

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
                "Коли вам зручно прийти? 📅",
                reply_markup=keyboard
            )
            return

        # ───── обработка callback даты ─────
        if callback_data and callback_data.startswith("date:"):
            key = callback_data.split(":")[1]

            if key in ("today", "tomorrow"):
                data["visit_date"] = get_date_label(key)
                await self.bot.send_message(
                    chat_id,
                    f"Обрана дата: {data['visit_date']}\n"
                    "Напишіть зручний час ⏰\n"
                    "Приклад: 15:30 або після 18:00"
                )
                return

            if key == "manual":
                await self.bot.send_message(
                    chat_id,
                    "Введіть дату у форматі:\n"
                    "ДД.ММ.РРРР\n\n"
                    "Приклад: 25.01.2026"
                )
                data["awaiting_manual_date"] = True
                return

        # ───── ручная дата ─────
        if data.get("awaiting_manual_date"):
            try:
                date = datetime.strptime(text, "%d.%m.%Y").date()
                if date < datetime.now().date():
                    raise ValueError
            except ValueError:
                await self.bot.send_message(
                    chat_id,
                    "❌ Некоректна дата або дата в минулому.\n"
                    "Спробуйте ще раз (ДД.ММ.РРРР)"
                )
                return

            data["visit_date"] = date.strftime("%d.%m.%Y")
            data.pop("awaiting_manual_date")

            await self.bot.send_message(
                chat_id,
                f"Обрана дата: {data['visit_date']}\n"
                "Напишіть зручний час ⏰"
            )
            return

        # ───── время ─────
        if "visit_time" not in data:
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
                "admin_comment": f"Дата: {data['visit_date']}, Час: {data['visit_time']}",
                "source": "telegram",
                "updated_at": ""
            }

            send_to_sheets(lead)
            notify_admin(lead)

            await self.bot.send_message(
                chat_id,
                "Дякуємо 🙌\n"
                "Ваша заявка прийнята, ми звʼяжемось з вами найближчим часом."
            )

            self.state.pop(chat_id, None)
