LEADS = []

def save_lead(lead: dict):
    LEADS.append(lead)

def format_lead_for_manager(lead: dict) -> str:
    return (
        "🆕 Новый лид\n"
        f"Статус: {lead['status']}\n"
        f"Услуга: {lead['service']}\n"
        f"Срочность: {lead['urgency']}\n"
        f"Тип клиента: {lead['client_type']}\n"
        f"Комментарий: {lead['comment']}"
    )
