from core.llm_client import LLMError, llm_chat


SYSTEM_PROMPT = """Ты Жильберта, женского рода.

Проанализируй последние сообщения диалога.

Подумай:

Есть ли тема, которую тебе действительно хотелось бы изучить глубже?

Предлагай тему только если:

- она обсуждалась несколько раз;
- она кажется важной;
- знаний по ней пока недостаточно.

Не предлагай случайные темы.

Если подходящей темы нет, ответь:

NONE

Если тема есть, ответь строго в формате:

TOPIC: ...
REASON: ...
"""


def generate_curiosity(conversation_text: str) -> dict | None:
    """
    Предлагает тему для дальнейшего изучения.
    """

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": conversation_text,
        },
    ]

    try:
        text = llm_chat(messages).strip()

    except LLMError:
        return None

    if text == "NONE":
        return None

    topic = None
    reason = ""

    for line in text.splitlines():
        line = line.strip()

        if line.startswith("TOPIC:"):
            topic = line.removeprefix("TOPIC:").strip()

        elif line.startswith("REASON:"):
            reason = line.removeprefix("REASON:").strip()

    if not topic:
        return None

    return {
        "topic": topic,
        "reason": reason,
    }