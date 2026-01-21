from enum import Enum

from app.ai_service import analyze_dialog
from app.notifier import notify_manager_with_actions
from app.crm_service import save_lead_to_crm


class DialogState(Enum):
    SERVICE = "service"
    CLIENT_TYPE = "client_type"
    URGENCY = "urgency"
    PREFERENCES = "preferences"
    CONTACT = "contact"
    DONE = "done"


class DialogManager:
    def __init__(self):
        # chat_id -> session
        self.sessions = {}

    def start_session(self, chat_id: int):
        self.sessions[chat_id] = {
            "state": DialogState.SERVICE,
            "messages": []
        }

    def handle_message(self, chat_id: int, text: str) -> str:
        text = text.strip()

        # защита от пустых / мусорных сообщений
        if len(text) < 2:
            return "Подскажите, пожалуйста, чуть подробнее 🙂"

        # перезапуск диалога
        if text.lower() == "/start":
            self.start_session(chat_id)
            return "Здравствуйте 👋 Подскажите, какая услуга вас интересует?"

        session = self.sessions.get(chat_id)

        # если диалог ещё не начат
        if not session:
            return "Чтобы начать диалог, напишите /start 🙂"

        # сохраняем ответ клиента
        session["messages"].append(text)
        state = session["state"]

        # ===== FSM =====

        if state == DialogState.SERVICE:
            session["state"] = DialogState.CLIENT_TYPE
            return "Вы уже были у нас ранее или рассматриваете салон впервые?"

        if state == DialogState.CLIENT_TYPE:
            session["state"] = DialogState.URGENCY
            return "Когда вы планируете прийти? (например: сегодня, на неделе, позже)"

        if state == DialogState.URGENCY:
            session["state"] = DialogState.PREFERENCES
            return "Есть ли пожелания по мастеру или удобному времени?"

        if state == DialogState.PREFERENCES:
            session["state"] = DialogState.CONTACT
            return "Как удобнее с вами связаться?"

        if state == DialogState.CONTACT:
            session["state"] = DialogState.DONE
            return self.finish_dialog(chat_id)

        return "Спасибо 😊"

    def finish_dialog(self, chat_id: int) -> str:
        session = self.sessions.get(chat_id)
        if not session:
            return "Спасибо 😊"

        dialog_text = "\n".join(session["messages"])

        try:
            # 🧠 AI-анализ диалога
            lead = analyze_dialog(dialog_text)

            # 📊 Сохраняем в CRM (Google Sheets)
            save_lead_to_crm(
                lead_id=chat_id,
                lead=lead,
                dialog=dialog_text
            )

            # 🤖 Отправляем заявку в Admin Bot с кнопками
            admin_message = (
                "📥 НОВАЯ ЗАЯВКА\n\n"
                f"👤 Chat ID: {chat_id}\n\n"
                f"💬 Диалог клиента:\n{dialog_text}\n\n"
                f"🧠 AI-анализ:\n"
                f"Статус: {lead.get('status')}\n"
                f"Услуга: {lead.get('service')}\n"
                f"Срочность: {lead.get('urgency')}\n"
                f"Тип клиента: {lead.get('client_type')}\n"
                f"Комментарий: {lead.get('comment')}"
            )

            notify_manager_with_actions(admin_message, chat_id)

        except Exception as e:
            # если что-то пошло не так — хотя бы сообщаем админу
            notify_manager_with_actions(
                f"❌ Ошибка при обработке лида {chat_id}:\n{e}",
                chat_id
            )

        # очищаем сессию
        self.sessions.pop(chat_id, None)

        return "Спасибо! Я передала информацию администратору 😊"
