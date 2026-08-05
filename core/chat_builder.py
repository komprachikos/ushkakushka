from config import MAX_LLM_CONTEXT


def build_chat_messages(system_prompt: str, messages: list):
    """
    Собирает список сообщений для отправки в LLM.

    Всегда оставляет:
      • один system prompt
      • последние MAX_LLM_CONTEXT сообщений user/assistant
    """

    chat_messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    history = [
        m
        for m in messages[1:]
        if m["role"] in ("user", "assistant")
    ]

    chat_messages.extend(history[-MAX_LLM_CONTEXT:])

    return chat_messages