import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def analyze_lead(user: dict) -> str:
    prompt = f"""
Клиент салона красоты.
Услуга: {user['service']}
Имя: {user['name']}

Сделай краткий вывод:
- тип клиента
- срочность
- как лучше с ним общаться
"""

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
    )

    return response.choices[0].message.content.strip()
