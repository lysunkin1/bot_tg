from app.notifier import notify_admin


class DialogManager:
    def __init__(self):
        self.state = {}

    async def handle_start(self, chat_id, send_message):
        self.state[chat_id] = {}
        await send_message(
            chat_id,
            "Здравствуйте 👋\nВыберите услугу:",
        )

    async def handle_message(self, chat_id, text, send_message):
        self.state.setdefault(chat_id, {})

        self.state[chat_id]["message"] = text

        await send_message(chat_id, "Спасибо! Передаю заявку администратору 🙌")

        await notify_admin(
            f"📩 Новая заявка\n\n"
            f"👤 Клиент ID: {chat_id}\n"
            f"💬 Сообщение: {text}"
        )
