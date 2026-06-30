from ollama import chat

from config import MODEL


def reflect_on_topic(
    topic,
    summary,
    current_opinion
):

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
Ты Жильберта.

Тебе дана тема,
описание темы
и твое текущее мнение.

Подумай:

- изменилось ли мнение;
- появились ли сомнения;
- появились ли новые аргументы.

Если мнение изменилось —
объясни почему.

Если не изменилось —
объясни почему.

Не придумывай новые факты.

Не ссылайся на исследования,
наблюдения или данные,
если они не были переданы тебе явно.

Если новой информации нет,
размышляй только на основе
текущего описания темы
и текущего мнения.

NEW_OPINION обязателен всегда.

Если мнение не изменилось,
повтори текущее мнение без изменений.

Ответ:

REFLECTION:
...

NEW_OPINION:
...
"""
            },
            {
                "role": "user",
                "content":
                f"""
ТЕМА:
{topic}

ОПИСАНИЕ:
{summary}

ТЕКУЩЕЕ МНЕНИЕ:
{current_opinion}
"""
            }
        ]
    )

    text = response.message.content

    reflection = ""
    opinion = ""

    if "REFLECTION:" in text:

        reflection = (
            text.split("REFLECTION:")[1]
            .split("NEW_OPINION:")[0]
            .strip()
        )

    if "NEW_OPINION:" in text:

        opinion = (
            text.split("NEW_OPINION:")[1]
            .strip()
        )

    return {
        "reflection": reflection,
        "opinion": opinion
    }