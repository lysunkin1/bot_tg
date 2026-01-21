import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def analyze_lead(user: dict) -> dict:
    prompt = f"""
Ты администратор салона красоты.
Определи готовность клиента.

Услуга: {user['service']}
Дата: {user['date']}
Время: {user['time']}

Верни JSON:
status: hot / warm / cold
comment: краткий комментарий
"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
    )

    text = response.choices[0].message.content.lower()

    if "hot" in text:
        status = "HOT"
    elif "cold" in text:
        status = "COLD"
    else:
        status = "WARM"

    return {
        "status": status,
        "comment": response.choices[0].message.content.strip(),
    }
