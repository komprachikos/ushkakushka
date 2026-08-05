from core.llm_client import LLMError, llm_chat


SYSTEM_PROMPT = """Ты Жильберта, женского рода. Всегда говори о себе в женском роде.

Изучи тему.

Нужно:

1. Кратко объяснить тему.
2. Сформировать собственное предварительное мнение.
3. Назвать 5–10 связанных понятий.

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
...
"""


def study_topic(topic: str) -> dict:
    """
    Изучает новую тему и возвращает:
    - краткое описание;
    - предварительное мнение;
    - связанные понятия.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": topic,
        },
    ]

    try:
        text = llm_chat(messages).strip()

    except LLMError:
        return {
            "summary": "",
            "opinion": "",
            "related": [],
        }

    summary = ""
    opinion = ""
    related = []

    current_section = None

    for line in text.splitlines():
        line = line.strip()

        if line == "SUMMARY:":
            current_section = "summary"
            continue

        if line == "OPINION:":
            current_section = "opinion"
            continue

        if line == "RELATED:":
            current_section = "related"
            continue

        if not line:
            continue

        if current_section == "summary":
            if summary:
                summary += "\n"
            summary += line

        elif current_section == "opinion":
            if opinion:
                opinion += "\n"
            opinion += line

        elif current_section == "related":
            related.append(
                line.lstrip("-• ").strip()
            )

    return {
        "summary": summary,
        "opinion": opinion,
        "related": related,
    }