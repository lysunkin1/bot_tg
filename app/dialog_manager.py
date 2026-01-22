from datetime import datetime

from app.ai_service import analyze_lead
from app.sheets_service import send_to_sheets
from app.notifier import notify_admin
from app.validators import (
    is_valid_name,
    is_valid_phone_ua,
    normalize_phone_ua,
    parse_visit_datetime,
)
from app.services import SERVICES


class DialogManager:
    def __init__(self, bot):
        self.bot = bot
        self.state = {}

    async def handle(self, chat_id: int, text: str = "", callback_data: str | None = None):
        data = self.state.get(chat_id)

        if text == "/start" or not data:
            self.state[chat_id] = {"step": "service"}
            await self.send_services(chat_id)
            return

        step = data["step"]

        # ─── УСЛУГА ───
        if step == "service" and callback_data:
            key = callback_data.split(":")[1]
            s = SERVICES[key]
            data["service"] = f"{s['title']} — {s['price']} грн"
            data["step"] = "name"
            await self.bot.send_message(chat_id, "Як вас звати?")
            return

        # ─── ІМʼЯ ───
        if step == "name":
            if not is_valid_name(text):
                await self.bot.send_message(chat_id, "❌ Введіть коректне імʼя")
                return
            data["client_name"] = text
            data["step"] = "phone"
            await self.bot.send_message(chat_id, "Введіть номер телефону 📞")
            return

        # ─── ТЕЛЕФОН ───
        if step == "phone":
            if not is_valid_phone_ua(text):
                await self.bot.send_message(chat_id, "❌ Невірний номер")
                return
            data["phone"] = normalize_phone_ua(text)
            data["step"] = "datetime"
            await self.bot.send_message(
                chat_id,
                "Введіть дату та час (дд.мм.рррр гг:хх)\nНапр: 25.01.2026 16:00"
            )
            return

        # ─── ДАТА + ЧАС ───
        if step == "datetime":
            visit = parse_visit_datetime(text)
            if not visit:
                await self.bot.send_message(chat_id, "❌ Некоректна дата або час")
                return

            data["visit_datetime"] = visit

            ai = analyze_lead(data)

            lead = {
                "created_at": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                "lead_id": chat_id,
                "client_name": data["client_name"],
                "phone": data["phone"],
                "service": data["service"],
                "visit_datetime": visit,
                "ai_status": ai["ai_status"],
                "ai_comment": ai["ai_comment"],
                "admin_status": "",
                "admin_comment": "",
                "source": "telegram",
                "updated_at": "",
            }

            send_to_sheets(lead)
            notify_admin(lead)

            await self.bot.send_message(chat_id, "Дякуємо! Заявка прийнята 🙌")
            self.state.pop(chat_id, None)

    async def send_services(self, chat_id: int):
        keyboard = {
            "inline_keyboard": [
                [{"text": f"{s['title']} — {s['price']} грн", "callback_data": f"service:{k}"}]
                for k, s in SERVICES.items()
            ]
        }
        await self.bot.send_message(chat_id, "Оберіть послугу 💅", reply_markup=keyboard)
