from core.llm_client import llm_chat, LLMError
from core.memory import save_memory
from mind.current_state import build_current_state
from mind.state_prompt import render_state
from core.logger import logger

MAX_HISTORY = 10


def process_message(messages, user_text):
    """
    Единый движок диалога. Используется и в CLI, и в Streamlit.

    Args:
        messages: список [{role, content}, ...], messages[0] — system prompt
        user_text: текст пользователя

    Returns:
        (answer, updated_messages, state, memory_context, full_system_prompt)

    Raises:
        LLMError: если модель не ответила
    """
    messages.append({"role": "user", "content": user_text})

    state = build_current_state(user_text)
    memory_context = render_state(state)

    chat_messages = [messages[0]]
    chat_messages.extend(messages[1:][-MAX_HISTORY:])

    full_system_prompt = (
        "Воспоминания и текущее внутреннее состояние Жильберты:\n\n"
        + memory_context +
        "\n\nИНСТРУКЦИЯ ДЛЯ ОТВЕТА:\n"
        "1. Отвечай по-новому каждый раз.\n"
        "2. Обязательно используй свои реальные убеждения из раздела 'Мои устоявшиеся убеждения'.\n"
        "3. Не повторяй одни и те же формулировки.\n"
        "4. Никаких личных примеров про пользователя."
    )

    chat_messages.append({
        "role": "system",
        "content": full_system_prompt
    })

    logger.debug(f"Chat messages count: {len(chat_messages)}")

    try:
        answer = llm_chat(chat_messages)
        logger.info(f"Ответ ИИ: {answer[:100]!r}")
    except LLMError:
        messages.pop()  # убираем user-сообщение при ошибке
        raise

    messages.append({"role": "assistant", "content": answer})
    save_memory(messages[1:])  # сохраняем всё кроме system prompt
    logger.debug("Память сохранена")

    return answer, messages, state, memory_context, full_system_prompt