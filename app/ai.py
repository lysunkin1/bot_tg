from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_lead(service, date, time):
    prompt = f"""
Клиент выбрал услугу: {service}
Дата: {date}
Время: {time}

Коротко прокомментируй готовность клиента к записи.
"""

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return r.choices[0].message.content.strip()
