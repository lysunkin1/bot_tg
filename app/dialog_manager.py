from typing import Dict


class DialogManager:
    """
    Управляет диалогом с клиентом.
    Пока без AI и CRM — только стабильная логика.
    """

    def __init__(self, bot):
        self.bot = bot

        # Простое хранение состояния диалога в памяти
        # chat_id -> step
        self.user_states: Dict[int, str] = {}

    async def handle_start(self, chat_id: int):
        """
        Обработка команды /start
        """
        self.user_states[chat_id] = "service"

        await self.bot.send_message(
            chat_id,
            "Здравствуйте 👋\n"
            "Подскажите, какая услуга вас интересует?"
        )

    async def handle_message(self, chat_id: int, text: str):
        """
        Обработка обычных сообщений
        """
        step = self.user_states.get(chat_id)

        if step is None:
            # Если пользователь написал без /start
            await self.handle_start(chat_id)
            return

        if step == "service":
            self.user_states[chat_id] = "date"

            await self.bot.send_message(
                chat_id,
                f"Хорошо 👍\n"
                f"Вы выбрали услугу: *{text}*\n\n"
                f"Когда вам удобно прийти?",
                parse_mode="Markdown"
            )
            return

        if step == "date":
            self.user_states[chat_id] = "contact"

            await self.bot.send_message(
                chat_id,
                f"Отлично 🗓\n"
                f"Записала: *{text}*\n\n"
                f"Как удобнее с вами связаться?",
                parse_mode="Markdown"
            )
            return

        if step == "contact":
            self.user_states.pop(chat_id, None)

            await self.bot.send_message(
                chat_id,
                "Спасибо! 😊\n"
                "Я передала информацию администратору.\n"
                "С вами свяжутся в ближайшее время."
            )
            return

        # Фолбэк на всякий случай
        await self.bot.send_message(
            chat_id,
            "Я вас поняла 🙂 Напишите /start, чтобы начать заново."
        )
