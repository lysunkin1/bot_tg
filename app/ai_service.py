from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_lead(lead: dict) -> dict:
    prompt = f"""
Ты CRM ассистент салона красоты.

Данные клиента:
Имя: {lead.get('name')}
Услуга: {lead.get('service')}
Дата: {lead.get('date')}
Время: {lead.get('time')}

Определи статус лида:
- HOT: записан на ближайшие 1–2 дня
- WARM: есть интерес, но не срочно
- COLD: далеко или не уверен

Ответь СТРОГО JSON:
{{"status": "hot|warm|cold", "comment": "короткий комментарий"}}
"""

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return eval(r.choices[0].message.content)
