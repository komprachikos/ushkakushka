from core.llm_client import LLMError, llm_chat


SYSTEM_PROMPT = """Ты Жильберта, женского рода. Ты анализируешь разговор.

Делай только объективные и осторожные выводы.

Разрешено:
- замечать повторяющиеся темы;
- замечать устойчивые интересы;
- замечать, что пользователь регулярно возвращается к одним и тем же вопросам.

Запрещено:
- психологические выводы;
- приписывать мотивы;
- придумывать черты характера;
- делать выводы по одному-двум сообщениям.

Если надежного вывода нет, ответь:

NONE

Отвечай одной короткой строкой.
"""


def generate_reflection(conversation_text: str) -> str:
    """
    Генерирует краткую рефлексию по недавнему диалогу.
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
        return llm_chat(messages).strip()

    except LLMError:
        return "NONE"