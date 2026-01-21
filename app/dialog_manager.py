from datetime import datetime, date
from app.ai import analyze_lead
from app.notifier import notify_admin
from app.sheets import send_to_sheets

class DialogManager:
    def __init__(self):
        self.sessions = {}

    def _get(self, chat_id):
        return self.sessions.setdefault(chat_id, {})

    async def handle_start(self, chat_id, send):
        self.sessions[chat_id] = {"chat_id": chat_id}
        await send(chat_id, "Здравствуйте 👋\nВыберите услугу:")

    async def handle_message(self, chat_id, text, send):
        s = self._get(chat_id)

        if "service" not in s:
            s["service"] = text
            await send(chat_id, "Выберите дату:")
            return

        if "date" not in s:
            s["date"] = text
            await send(chat_id, "Выберите время:")
            return

        if "time" not in s:
            s["time"] = text
            await send(chat_id, "Как вас зовут?")
            return

        if "name" not in s:
            s["name"] = text
            await send(chat_id, "Введите номер телефона 📞")
            return

        if "phone" not in s:
            s["phone"] = text
            await self.finish(chat_id, send)

    async def finish(self, chat_id, send):
        s = self.sessions[chat_id]

        # ---- статус СЧИТАЕМ КОДОМ ----
        selected = datetime.fromisoformat(
            f"{s['date']} {s['time']}"
        )
        days = (selected.date() - date.today()).days

        if days <= 1:
            status = "HOT"
        elif days <= 5:
            status = "WARM"
        else:
            status = "COLD"

        # ---- ИИ ТОЛЬКО КОММЕНТАРИЙ ----
        comment = analyze_lead(
            service=s["service"],
            date=s["date"],
            time=s["time"]
        )

        lead = {
            "chat_id": chat_id,
            "name": s["name"],
            "phone": s["phone"],
            "service": s["service"],
            "date": s["date"],
            "time": s["time"],
            "status": status,
            "comment": comment,
        }

        notify_admin(lead)
        send_to_sheets(lead)

        await send(chat_id, "Спасибо! 🙌 Заявка передана администратору.")
        del self.sessions[chat_id]
