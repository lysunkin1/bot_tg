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

        step = data["step"]

        # ─── ВИБІР ПОСЛУГИ ───
        if step == "service":
            if callback_data and callback_data.startswith("service:"):
                key = callback_data.split(":")[1]
                s = SERVICES[key]
                data["service"] = f"{s['title']} — {s['price']} грн"
                data["step"] = "name"
                await self.bot.send_message(chat_id, "Як вас звати?")
            return

        # ─── ІМʼЯ ───
        if step == "name":
            data["client_name"] = text
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
                    "❌ Невірний формат номера.\nСпробуйте ще раз."
                )
                return

            data["phone"] = normalize_phone_ua(text)
            data["step"] = "datetime"
            await self.bot.send_message(
                chat_id,
                "Коли вам зручно прийти?\n"
                "Приклад: 25.01 о 16:00"
            )
            return

        # ─── ДАТА + ЧАС ───
        if step == "datetime":
            data["visit_datetime"] = text

            ai = analyze_lead({
                "service": data["service"],
                "phone": data["phone"],
                "visit_datetime": data["visit_datetime"]
            })

            lead = {
                "created_at": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "lead_id": chat_id,
                "client_name": data["client_name"],
                "phone": data["phone"],
                "service": data["service"],
                "visit_datetime": data["visit_datetime"],
                "ai_status": ai["ai_status"],
                "ai_comment": ai["ai_comment"],
                "admin_status": "",
                "admin_comment": "",
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
