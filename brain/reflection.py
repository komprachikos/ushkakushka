from ollama import chat

from config import MODEL


def generate_reflection(conversation_text):
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
Ты анализируешь разговор. Делай ТОЛЬКО объективные и осторожные выводы.

Разрешено:
- Замечать повторяющиеся темы и прямые интересы
- Замечать, что пользователь часто спрашивает об одном и том же

Строго запрещено:
- Психологические выводы ("стремление к гармонии", "осознанность" и т.п.)
- Придумывать мотивы и черты характера
- Делать обобщения на основе одного-двух сообщений

Если надёжного факта нет — отвечай ровно: NONE

Отвечай одной короткой строкой.
"""
            },
            {
                "role": "user",
                "content": conversation_text
            }
        ]
    )

    return response.message.content.strip()