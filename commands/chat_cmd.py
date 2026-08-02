from core.logger import logger
from core.profile_memory import add_fact
from core.prompts_builder import build_system_prompt
from core.journal import add_thought
from core.curiosity import add_curiosity
from brain.fact_extractor import extract_fact
from brain.reflection import generate_reflection
from brain.curiosity import generate_curiosity
from core.llm_client import LLMError
from core.chat_engine import process_message


def handle_chat(session, user_text):
    logger.info(f"Пользователь: {user_text[:80]!r}")

    fact = extract_fact(user_text)
    logger.debug(f"Факт: {fact!r}")

    if fact != "NONE":
        add_fact(fact)
        session.messages[0]["content"] = build_system_prompt()
        logger.info(f"Новый факт: {fact}")
        print("\n[PROFILE RELOADED]\n")
        print(f"\n[Новый факт] {fact}\n")

    session.message_counter += 1
    logger.debug(f"Счётчик: {session.message_counter}")

    try:
        answer, session.messages, _, _, _ = process_message(
            session.messages, user_text
        )
    except LLMError as e:
        logger.error(f"Ошибка LLM: {e}")
        print(f"\n[ОШИБКА LLM] {e}")
        print("Пропускаю этот запрос. Попробуй ещё раз.\n")
        return True

    print(f"\nИИ: {answer}\n")

    if session.message_counter % 25 == 0:
        logger.info("Триггер рефлексии")
        print("[REFLECTION TRIGGERED]")
        recent_messages = session.messages[-20:]
        conversation_text = "\n".join(
            f"{msg['role']}: {msg['content']}" for msg in recent_messages
        )
        thought = generate_reflection(conversation_text)
        logger.debug(f"Рефлексия: {thought!r}")
        if thought != "NONE" and len(thought) < 180:
            add_thought(thought)
            logger.info(f"Мысль: {thought}")
            print(f"\n[Размышление Жильберты] {thought}\n")

        curiosity = generate_curiosity(conversation_text)
        if curiosity:
            add_curiosity(curiosity["topic"], curiosity["reason"])
            logger.info(f"Любопытство: {curiosity['topic']}")
            print(f"\n[Жильберта заинтересовалась]")
            print(f"Тема: {curiosity['topic']}")
            print(f"Причина: {curiosity['reason']}\n")
            print(f"Если хочешь, чтобы я изучила эту тему — напиши:")
            print(f"/teach {curiosity['topic']}")

    return True