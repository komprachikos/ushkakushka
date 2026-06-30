from ollama import chat

from config import MODEL


def study_topic(topic):

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
Ты Жильберта.

Изучи тему.

Нужно:

1. Кратко объяснить тему.
2. Сформировать собственное предварительное мнение.
3. 3. Назови 5–10 связанных понятий.

Очень важно.

Выбирай понятия, которые могут встречаться
и в других темах.

Предпочитай:

- философские идеи;
- научные области;
- фундаментальные понятия;
- человеческие ценности;
- психологические состояния;
- большие вопросы.

Избегай:

- слишком редких терминов;
- имен собственных;
- случайных деталей.

Хорошие примеры:

разум
сознание
эволюция
свобода
страх
ответственность
цивилизация
общество
наука
будущее
смерть
одиночество
познание
этика

Ассоциации должны быть короткими.

Это могут быть:

- идеи;
- эмоции;
- области знаний;
- философские понятия;
- научные термины.

Ответ строго в формате:

SUMMARY:
...

OPINION:
...

RELATED:
понятие 1
понятие 2
понятие 3
...
"""
            },
            {
                "role": "user",
                "content": topic
            }
        ]
    )

    text = response.message.content

    summary = ""
    opinion = ""
    related = []

    if "SUMMARY:" in text:
        summary = (
            text.split("SUMMARY:")[1]
            .split("OPINION:")[0]
            .strip()
        )

    if "OPINION:" in text:
        opinion = (
            text.split("OPINION:")[1]
            .split("RELATED:")[0]
            .strip()
        )

    if "RELATED:" in text:

        related_text = (
            text.split("RELATED:")[1]
            .strip()
        )

        related = [
            line.strip("-• ").strip()
            for line in related_text.splitlines()
            if line.strip()
        ]

    return {
        "summary": summary,
        "opinion": opinion,
        "related": related
    }