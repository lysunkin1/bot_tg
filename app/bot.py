import requests

from app.dialog_manager import DialogManager
from app.config import TELEGRAM_API



dialog_manager = DialogManager()


async def handle_update(update: dict):
    """
    Точка входа для всех апдейтов от Telegram
    """

    # 1️⃣ Обработка callback-кнопок (админ)
    if "callback_query" in update:
        handle_callback(update["callback_query"])
        return

    # 2️⃣ Обычные сообщения
    if "message" not in update:
        return

    message = update["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text")

    if not text:
        return

    reply = dialog_manager.handle_message(chat_id, text)
    send_message(chat_id, reply)


def handle_callback(callback: dict):
    """
    Обработка нажатий кнопок администратором
    """
    data = callback.get("data")
    admin_chat_id = callback["message"]["chat"]["id"]

    if not data:
        return

    # 📅 Кнопка "Записать"
    if data.startswith("book:"):
        client_chat_id = data.split(":")[1]

        send_message(
            admin_chat_id,
            f"✅ Лид с Chat ID {client_chat_id} отмечен как *ЗАПИСАННЫЙ*.\n"
            f"Дальше можно связаться с клиентом напрямую.",
        )

        answer_callback(callback["id"], "Лид отмечен как записанный")

    # 📞 Кнопка "Перезвонить"
    elif data.startswith("call:"):
        client_chat_id = data.split(":")[1]

        send_message(
            admin_chat_id,
            f"📞 Лид с Chat ID {client_chat_id} отмечен как *НУЖЕН ЗВОНОК*.",
        )

        answer_callback(callback["id"], "Лид отмечен для звонка")


def send_message(chat_id: int, text: str):
    """
    Отправка обычного текстового сообщения
    """
    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }
    )


def answer_callback(callback_id: str, text: str):
    """
    Обязательный ответ Telegram при нажатии кнопки
    (иначе кнопка будет "крутиться")
    """
    requests.post(
        f"{TELEGRAM_API}/answerCallbackQuery",
        json={
            "callback_query_id": callback_id,
            "text": text,
            "show_alert": False
        }
    )
