from app.ai_service import analyze_lead
from app.sheets_service import send_to_sheets

class DialogManager:
    def __init__(self, bot):
        self.bot = bot
        self.state = {}

    async def handle_start(self, chat_id, send):
        self.state[chat_id] = {}
        await send(chat_id, "Здравствуйте 👋\nВыберите услугу:")

    async def finalize(self, chat_id, send):
        lead = self.state[chat_id]

        ai = analyze_lead(lead)

        lead["status"] = ai["status"].upper()
        lead["comment"] = ai["comment"]

        # ⬇️ ВАЖНО: client_id НЕ ТЕРЯЕМ
        lead["client_id"] = chat_id

        send_to_sheets(lead)

        await self.bot.send_message(
            chat_id=self.bot.admin_chat_id,
            text=(
                "📩 Новая заявка\n\n"
                f"👤 Имя: {lead['name']}\n"
                f"📞 Телефон: {lead['phone']}\n"
                f"💼 Услуга: {lead['service']}\n"
                f"📅 Дата: {lead['date']} {lead['time']}\n\n"
                f"🔥 Статус: {lead['status']}\n"
                f"🤖 Комментарий: {lead['comment']}"
            ),
            reply_markup=self._admin_keyboard()
        )

        await send(chat_id, "Спасибо! 🙌\nЗаявка передана администратору.")

    def _admin_keyboard(self):
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        return InlineKeyboardMarkup([
            [InlineKeyboardButton("📅 Записать", callback_data="approve")],
            [InlineKeyboardButton("📞 Перезвонить", callback_data="call")],
            [InlineKeyboardButton("❌ Отказ", callback_data="reject")]
        ])
