import json
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Ты — AI-ассистент администратора салона красоты.
Проанализируй диалог клиента и верни JSON СТРОГО в таком формате:

{
  "status": "hot | warm | cold",
  "service": "кратко",
  "urgency": "когда планирует",
  "client_type": "new | returning",
  "comment": "краткий вывод"
}

Правила:
- hot — хочет прийти скоро и готов к контакту
- warm — интерес есть, но без срочности
- cold — просто интересуется
- Никакого текста вне JSON
"""

def analyze_dialog(dialog: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": dialog}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "status": "warm",
            "service": "не определено",
            "urgency": "не указано",
            "client_type": "new",
            "comment": "AI не смог корректно распарсить ответ"
        }
