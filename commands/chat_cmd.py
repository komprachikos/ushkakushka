from core.logger import logger
from core.llm_client import LLMError
from core.chat_engine import process_message


def handle_chat(session, user_text):
    logger.info(f"Пользователь: {user_text[:80]!r}")

    try:
        answer, session.messages, _, _, _, session.message_counter, reflection, curiosity = process_message(
            session.messages, user_text, session.message_counter
        )
    except LLMError as e:
        logger.error(f"Ошибка LLM: {e}")
        print(f"\n[ОШИБКА LLM] {e}")
        print("Пропускаю этот запрос. Попробуй ещё раз.\n")
        return True

    print(f"\nИИ: {answer}\n")

    if reflection:
        print(f"\n[Размышление Жильберты] {reflection}\n")

    if curiosity:
        print(f"\n[Жильберта заинтересовалась]")
        print(f"Тема: {curiosity['topic']}")
        print(f"Причина: {curiosity['reason']}\n")
        print(f"Если хочешь, чтобы я изучила эту тему — напиши:")
        print(f"/teach {curiosity['topic']}")

    return True