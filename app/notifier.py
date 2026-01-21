from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from app.config import ADMIN_CHAT_ID

async def notify_admin(bot, lead: dict):
    text = (
        "📩 Новая заявка\n\n"
        f"👤 Имя: {lead['name']}\n"
        f"📞 Телефон: {lead['phone']}\n"
        f"💼 Услуга: {lead['service']}\n\n"
        f"🔥 Статус: {lead['status']}\n"
        f"💬 Комментарий: {lead['comment']}"
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Записать", callback_data="confirm")],
        [InlineKeyboardButton("📞 Перезвонить", callback_data="call")],
        [InlineKeyboardButton("❌ Отказ", callback_data="reject")]
    ])

    await bot.send_message(ADMIN_CHAT_ID, text, reply_markup=keyboard)
