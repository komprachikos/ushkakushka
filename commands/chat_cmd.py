from core.logger import logger
from core.memory import save_memory
from core.profile_memory import add_fact
from core.prompts_builder import build_system_prompt
from core.journal import add_thought
from core.curiosity import add_curiosity
from brain.fact_extractor import extract_fact
from brain.reflection import generate_reflection
from brain.curiosity import generate_curiosity
from mind.current_state import build_current_state
from mind.state_prompt import render_state
from core.llm_client import llm_chat, LLMError


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

    session.messages.append({"role": "user", "content": user_text})
    session.message_counter += 1
    logger.debug(f"Счётчик: {session.message_counter}")

    state = build_current_state(user_text)
    memory_context = render_state(state)

    chat_messages = [session.messages[0]]
    chat_messages.extend(session.messages[1:][-10:])

    if memory_context:
        logger.debug("Контекст памяти найден")
        print("\n[MEMORY FOUND]")
        print(memory_context)
        print()

    chat_messages.append({
        "role": "system",
        "content": (
            "Воспоминания и текущее внутреннее состояние Жильберты:\n\n"
            + memory_context +
            "\n\nИНСТРУКЦИЯ ДЛЯ ОТВЕТА:\n"
            "1. Отвечай по-новому каждый раз.\n"
            "2. Обязательно используй свои реальные убеждения из раздела 'Мои устоявшиеся убеждения'.\n"
            "3. Не повторяй одни и те же формулировки.\n"
            "4. Никаких личных примеров про пользователя."
        )
    })

    print("\n===== CHAT MESSAGES =====\n")
    for i, msg in enumerate(chat_messages):
        print(f"{i}: {msg['role']}")
        print(msg["content"][:300])
        print("-" * 40)

    try:
        answer = llm_chat(chat_messages)
        logger.info(f"Ответ ИИ: {answer[:100]!r}")
    except LLMError as e:
        logger.error(f"Ошибка LLM: {e}")
        print(f"\n[ОШИБКА LLM] {e}")
        print("Пропускаю этот запрос. Попробуй ещё раз.\n")
        session.messages.pop()
        return True

    print(f"\nИИ: {answer}\n")
    session.messages.append({"role": "assistant", "content": answer})
    save_memory(session.messages[1:])
    logger.debug("Память сохранена")

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