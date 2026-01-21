from typing import Dict, Callable, Awaitable


class DialogManager:
    """
    Управляет логикой диалога.
    Не зависит напрямую от Telegram API.
    """

    def __init__(self):
        # chat_id -> step
        self.user_states: Dict[int, str] = {}

    async def handle_start(
        self,
        chat_id: int,
        send_message: Callable[[int, str], Awaitable[None]],
    ):
        self.user_states[chat_id] = "service"

        await send_message(
            chat_id,
            "Здравствуйте 👋\n"
            "Подскажите, какая услуга вас интересует?"
        )

    async def handle_message(
        self,
        chat_id: int,
        text: str,
        send_message: Callable[[int, str], Awaitable[None]],
    ):
        step = self.user_states.get(chat_id)

        if step is None:
            await self.handle_start(chat_id, send_message)
            return

        if step == "service":
            self.user_states[chat_id] = "date"

            await send_message(
                chat_id,
                f"Хорошо 👍\n"
                f"Вы выбрали услугу: {text}\n\n"
                f"Когда вам удобно прийти?"
            )
            return

        if step == "date":
            self.user_states[chat_id] = "contact"

            await send_message(
                chat_id,
                f"Отлично 🗓\n"
                f"Записала: {text}\n\n"
                f"Как удобнее с вами связаться?"
            )
            return

        if step == "contact":
            self.user_states.pop(chat_id, None)

            await send_message(
                chat_id,
                "Спасибо! 😊\n"
                "Я передала информацию администратору.\n"
                "С вами свяжутся в ближайшее время."
            )
            return

        await send_message(
            chat_id,
            "Напишите /start, чтобы начать заново 🙂"
        )
