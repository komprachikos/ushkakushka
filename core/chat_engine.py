from core.llm_client import llm_chat, LLMError
from core.memory import save_memory
from core.prompts_builder import build_system_prompt
from mind.current_state import build_current_state
from mind.state_prompt import render_state
from brain.fact_extractor import extract_fact
from brain.reflection import generate_reflection
from brain.curiosity import generate_curiosity
from core.journal import add_thought
from core.curiosity import add_curiosity
from core.profile_memory import add_fact
from core.logger import logger
from config import MAX_HISTORY, MAX_LLM_CONTEXT, TEMPERATURE, REFLECTION_INTERVAL, THOUGHT_MAX_LEN


def process_message(messages, user_text, message_counter=0):
    """
    Единый движок диалога. Используется и в CLI, и в Streamlit.

    Args:
        messages: список [{role, content}, ...], messages[0] — system prompt
        user_text: текст пользователя
        message_counter: текущий счётчик сообщений (для триггера рефлексии)

    Returns:
        (answer, updated_messages, state, memory_context, full_system_prompt,
         message_counter, reflection_thought, curiosity_item)

    Raises:
        LLMError: если модель не ответила
    """
    # Работаем с копией, чтобы не портить входной список при ошибке
    local_messages = list(messages)

    # 1. Извлечение фактов о пользователе (раньше было только в CLI)
    fact = extract_fact(user_text)
    logger.debug(f"Факт: {fact!r}")
    if fact != "NONE":
        add_fact(fact)
        # Пересобираем system prompt с новым фактом
        local_messages[0] = {"role": "system", "content": build_system_prompt()}
        logger.info(f"Новый факт: {fact}")

    # 2. Добавляем сообщение пользователя (единственное место в коде)
    local_messages.append({"role": "user", "content": user_text})

    # 3. Увеличиваем счётчик
    message_counter += 1
    logger.debug(f"Счётчик: {message_counter}")

    # АВТО-КОНФЛИКТ: проверяем, не противоречит ли пользователь своим убеждениям
    conflict_topic = None
    recent_user_text = "\n".join(
        m["content"] for m in local_messages[-10:] if m["role"] == "user"
    )
    if recent_user_text:
        from core.embeddings import find_similar_topics, get_embedding
        from core.knowledge import get_current_opinion
        from config import TOP_K_SIMILAR, SIMILARITY_THRESHOLD
        import numpy as np
        
        similar = find_similar_topics(recent_user_text, top_k=TOP_K_SIMILAR, threshold=SIMILARITY_THRESHOLD)
        if similar:
            user_emb = np.array(get_embedding(recent_user_text))
            for topic, score in similar:
                opinion = get_current_opinion(topic)
                if not opinion:
                    continue
                opinion_emb = np.array(get_embedding(opinion["text"]))
                cos = float(
                    np.dot(user_emb, opinion_emb) /
                    (np.linalg.norm(user_emb) * np.linalg.norm(opinion_emb))
                )
                if cos < 0.35:
                    conflict_topic = topic
                    logger.info(f"Конфликт мнений: {topic} (cos={cos:.2f})")
                    break

    # 4. Строим текущее состояние
    state = build_current_state(user_text, conflict_topic=conflict_topic)
    memory_context = render_state(state)

    # 5. Собираем единый system prompt в начало
    base_system = local_messages[0]["content"]
    full_system_prompt = (
        base_system + "\n\n"
        + memory_context + "\n\n"
        + "ИНСТРУКЦИЯ ДЛЯ ОТВЕТА:\n"
        "1. Отвечай по-новому каждый раз.\n"
        "2. Обязательно используй свои реальные убеждения из раздела 'Мои устоявшиеся убеждения'.\n"
        "3. Не повторяй одни и те же формулировки.\n"
        "4. Никаких личных примеров про пользователя."
    )

    # 6. Формируем сообщения для LLM: один system + последняя история user/assistant
    chat_messages = [{"role": "system", "content": full_system_prompt}]
    history = [m for m in local_messages[1:] if m["role"] in ("user", "assistant")]
    chat_messages.extend(history[-MAX_LLM_CONTEXT:])

    logger.debug(f"Chat messages count: {len(chat_messages)}")

    # 7. Вызываем LLM
    try:
        answer = llm_chat(chat_messages, temperature=TEMPERATURE)
        logger.info(f"Ответ ИИ: {answer[:100]!r}")
    except LLMError:
        # Не мутируем входной список — просто пробрасываем ошибку
        raise

    # 8. Добавляем ответ ассистента
    local_messages.append({"role": "assistant", "content": answer})

    # 9. Сохраняем память (всё кроме system prompt)
    save_memory(local_messages[1:])
    logger.debug("Память сохранена")

    # 10. Рефлексия и любопытство (раньше было только в CLI)
    reflection_thought = None
    curiosity_item = None

        # АВТО-РЕФЛЕКСИЯ: проверяем, не противоречит ли пользователь своим убеждениям
    from core.embeddings import find_similar_topics, get_embedding
    from core.knowledge import get_current_opinion
    import numpy as np

    recent_user_text = "\n".join(
        m["content"] for m in local_messages[-10:] if m["role"] == "user"
    )
    if recent_user_text:
        similar = find_similar_topics(recent_user_text, top_k=3, threshold=0.4)
        for topic, score in similar:
            opinion = get_current_opinion(topic)
            if not opinion:
                continue
            
            user_emb = np.array(get_embedding(recent_user_text))
            opinion_emb = np.array(get_embedding(opinion["text"]))
            cos = float(
                np.dot(user_emb, opinion_emb) /
                (np.linalg.norm(user_emb) * np.linalg.norm(opinion_emb))
            )
            
            if cos < 0.35:  # пользователь говорит что-то сильно другое
                state["conflict_topic"] = topic
                logger.info(f"Конфликт мнений: {topic} (cos={cos:.2f})")
                break  # один конфликт за раз

    if message_counter % REFLECTION_INTERVAL == 0:
        logger.info("Триггер рефлексии")
        from core.profile_memory import consolidate_facts
        consolidate_facts()
        recent_messages = local_messages[-20:]
        conversation_text = "\n".join(
            f"{msg['role']}: {msg['content']}" for msg in recent_messages
        )

        thought = generate_reflection(conversation_text)
        logger.debug(f"Рефлексия: {thought!r}")
        if thought != "NONE" and len(thought) < THOUGHT_MAX_LEN:
            add_thought(thought)
            reflection_thought = thought
            logger.info(f"Мысль: {thought}")

        curiosity = generate_curiosity(conversation_text)
        if curiosity:
            add_curiosity(curiosity["topic"], curiosity["reason"])
            curiosity_item = curiosity
            logger.info(f"Любопытство: {curiosity['topic']}")

    return (
        answer, local_messages, state, memory_context,
        full_system_prompt, message_counter, reflection_thought, curiosity_item
    )