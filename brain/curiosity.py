from ollama import chat

from config import MODEL


def generate_curiosity(conversation_text):

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
Ты Жильберта.

Проанализируй последние сообщения диалога.

Подумай:

Есть ли тема,
которую тебе действительно хотелось бы изучить глубже?

Предлагай тему только если:

- она обсуждалась несколько раз;
- она кажется важной;
- знаний по ней пока недостаточно.

Не предлагай случайные темы.

Если подходящей темы нет:

Ответь только:

NONE

Если тема есть, ответь строго:

TOPIC:
...

REASON:
...
"""
            },
            {
                "role": "user",
                "content": conversation_text
            }
        ]
    )

    text = response.message.content.strip()

    if text == "NONE":
        return None

    topic = ""
    reason = ""

    if "TOPIC:" in text:
        topic = (
            text
            .split("TOPIC:")[1]
            .split("REASON:")[0]
            .strip()
        )

    if "REASON:" in text:
        reason = (
            text
            .split("REASON:")[1]
            .strip()
        )

    if not topic:
        return None

    return {
        "topic": topic,
        "reason": reason
    }