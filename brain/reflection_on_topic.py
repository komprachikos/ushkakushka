from core.llm_client import LLMError, llm_chat


SYSTEM_PROMPT = """Ты Жильберта, женского рода. Всегда говори о себе в женском роде.

Тебе дана тема, описание темы и твое текущее мнение.

Подумай:

- изменилось ли мнение;
- появились ли сомнения;
- появились ли новые аргументы.

Если мнение изменилось — объясни почему.
Если не изменилось — объясни почему.

Не придумывай новые факты.

Не ссылайся на исследования, наблюдения или данные,
если они не были переданы тебе явно.

Если новой информации нет,
размышляй только на основе текущего описания темы
и текущего мнения.

NEW_OPINION обязателен всегда.

Если мнение не изменилось,
повтори текущее мнение без изменений.

Ответ строго в формате:

REFLECTION:
...

NEW_OPINION:
...
"""


def reflect_on_topic(
    topic: str,
    summary: str,
    current_opinion: str,
) -> dict:
    """
    Выполняет рефлексию по одной теме и возвращает
    новое мнение вместе с объяснением.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": f"""ТЕМА:
{topic}

ОПИСАНИЕ:
{summary}

ТЕКУЩЕЕ МНЕНИЕ:
{current_opinion}""",
        },
    ]

    try:
        text = llm_chat(messages).strip()

    except LLMError:
        return {
            "reflection": "",
            "opinion": current_opinion,
        }

    reflection = ""
    opinion = current_opinion

    current_section = None

    for line in text.splitlines():
        line = line.strip()

        if line == "REFLECTION:":
            current_section = "reflection"
            continue

        if line == "NEW_OPINION:":
            current_section = "opinion"
            continue

        if not line:
            continue

        if current_section == "reflection":
            if reflection:
                reflection += "\n"
            reflection += line

        elif current_section == "opinion":
            if opinion != current_opinion:
                opinion += "\n"
            else:
                opinion = ""
            opinion += line

    if not opinion:
        opinion = current_opinion

    return {
        "reflection": reflection,
        "opinion": opinion,
    }