from ollama import chat
from config import MODEL
from core.llm_client import llm_chat, LLMError
from core.memory import load_memory, save_memory
from core.profile_memory import load_profile, add_fact
from core.prompts_builder import build_system_prompt
from core.journal import add_thought, get_recent_thoughts, load_journal
from core.knowledge import get_topics, get_knowledge, get_current_opinion, add_knowledge
from core.pending_study import set_pending, load_pending, clear_pending
from core.pending_reflection import save_pending_reflection, load_pending_reflection, clear_pending_reflection
from core.embeddings import ensure_topic_embedding
from core.curiosity import add_curiosity
from core.logger import logger
from brain.fact_extractor import extract_fact
from brain.reflection import generate_reflection
from brain.teacher import study_topic
from brain.reflection_on_topic import reflect_on_topic
from brain.curiosity import generate_curiosity
from mind.current_state import build_current_state
from mind.state_prompt import render_state
import atexit


# ============ СОСТОЯНИЕ ============

saved_messages = load_memory()
message_counter = len(saved_messages)

messages = [
    {"role": "system", "content": build_system_prompt()}
]
messages.extend(saved_messages)


# ============ ХЕЛПЕРЫ ============

def _handle_pending_reflection():
    pending = load_pending_reflection()
    if not pending:
        return False
    old_opinion = pending.get("old_opinion", "").strip()
    new_opinion = pending.get("new_opinion", "").strip()
    if old_opinion == new_opinion:
        print("\nМнение не изменилось. Новая версия не сохранена.\n")
        clear_pending_reflection()
        return True
    add_knowledge(
        topic=pending["topic"],
        summary=pending["summary"],
        opinion=pending["new_opinion"],
        related=pending.get("related", [])
    )
    ensure_topic_embedding(pending["topic"])
    clear_pending_reflection()
    print("\nНовая версия мнения сохранена.\n")
    logger.info(f"Рефлексия сохранена: {pending['topic']}")
    return True


def _handle_pending_study():
    pending = load_pending()
    if not pending:
        return False
    add_knowledge(
        topic=pending["topic"],
        summary=pending["summary"],
        opinion=pending["opinion"],
        related=pending.get("related", [])
    )
    ensure_topic_embedding(pending["topic"])
    clear_pending()
    print("\nЗнание сохранено.\n")
    logger.info(f"Знание сохранено: {pending['topic']}")
    return True


def _save_on_exit():
    logger.info("Сохранение памяти перед выходом...")
    try:
        save_memory(messages[1:])
        logger.info("Память сохранена.")
    except Exception as e:
        logger.error(f"Ошибка сохранения: {e}")


# ============ КОМАНДЫ ============

def cmd_knowledge():
    print("\n=== KNOWLEDGE ===\n")
    topics = get_topics()
    if not topics:
        print("Пока нет сохранённых знаний.\n")
    else:
        for topic in topics:
            print(f"- {topic}")
        print()


def cmd_knowledge_detail(topic):
    knowledge = get_knowledge(topic)
    if knowledge is None:
        print("\nТема не найдена.\n")
        return
    print("\n=== KNOWLEDGE ===\n")
    print(f"Тема: {knowledge['topic']}")
    print(f"\nОписание:\n{knowledge['summary']}")
    opinion = get_current_opinion(topic)
    if opinion:
        print(f"\nТекущее мнение:\n{opinion['text']}")
    print(f"\nВерсий мнения: {len(knowledge.get('opinions', []))}")
    print("\nИстория:")
    for opinion in knowledge.get("opinions", []):
        print(f"- {opinion['date']} | {opinion['text']}")
    print()
    print()


def cmd_teach(topic):
    logger.info(f"/teach {topic}")
    result = study_topic(topic)
    set_pending(
        topic=topic,
        summary=result["summary"],
        opinion=result["opinion"],
        related=result["related"]
    )
    print("\n=== STUDY RESULT ===\n")
    print(f"Тема: {topic}")
    print(f"\nОписание:\n{result['summary']}")
    print(f"\nПредварительное мнение:\n{result['opinion']}")
    print("\nRELATED:")
    for item in result["related"]:
        print(f"- {item}")
    print("\nСохранить знание: /approve")
    print("Отменить: /reject\n")


def cmd_reflect(topic):
    logger.info(f"/reflect {topic}")
    knowledge = get_knowledge(topic)
    if knowledge is None:
        print("\nТема не найдена.\n")
        return
    if not knowledge.get("opinions"):
        print("\nПо этой теме ещё нет мнения.\n")
        return
    current_opinion = knowledge["opinions"][-1]["text"]
    result = reflect_on_topic(topic, knowledge["summary"], current_opinion)
    print("\n=== REFLECTION ===\n")
    print(f"Тема: {topic}")
    print(f"\nРазмышление:\n{result['reflection']}")
    print(f"\nНовое мнение:\n{result['opinion']}")
    save_pending_reflection({
        "topic": topic,
        "summary": knowledge["summary"],
        "old_opinion": current_opinion,
        "new_opinion": result["opinion"],
        "related": knowledge.get("related", [])
    })
    print("\nСохранить: /approve\nОтменить: /reject\n")


def cmd_approve():
    if _handle_pending_reflection():
        return
    if _handle_pending_study():
        return
    print("\nНет ожидающих операций.\n")


def cmd_reject():
    clear_pending()
    print("\nИзучение отменено.\n")


def cmd_brain():
    profile = load_profile()
    print("\n=== PROFILE ===")
    print(f"Имя: {profile['name']}")
    print("\n=== FACTS ===")
    for fact in profile.get("facts", [])[-5:]:
        print(f"- {fact}")
    print("\n=== THOUGHTS ===")
    thoughts = get_recent_thoughts()
    for item in thoughts:
        print(f"- {item['thought']}")
    print()


def cmd_stats():
    profile = load_profile()
    journal = load_journal()
    print("\n=== STATS ===")
    print(f"Сообщений: {len(saved_messages)}")
    print(f"Фактов: {len(profile.get('facts', []))}")
    print(f"Размышлений: {len(journal)}")
    if profile.get("facts"):
        print(f"\nПоследний факт:\n{profile['facts'][-1]}")
    if journal:
        print(f"\nПоследнее размышление:\n{journal[-1]['thought']}")
    print()


# ============ ОСНОВНОЙ ДИАЛОГ ============

def cmd_chat(user_text):
    global message_counter

    # Извлечение фактов
    fact = extract_fact(user_text)
    logger.debug(f"Факт: {fact!r}")

    if fact != "NONE":
        add_fact(fact)
        messages[0]["content"] = build_system_prompt()
        logger.info(f"Новый факт: {fact}")
        print("\n[PROFILE RELOADED]\n")
        print(f"\n[Новый факт] {fact}\n")

    messages.append({"role": "user", "content": user_text})
    message_counter += 1
    logger.debug(f"Счётчик: {message_counter}")

    # Контекст
    state = build_current_state(user_text)
    memory_context = render_state(state)

    chat_messages = [messages[0]]
    chat_messages.extend(messages[1:][-10:])

    if memory_context:
        print("\n[MEMORY FOUND]")
        print(memory_context)
        print()

    chat_messages.append({
        "role": "system",
        "content":
        "Воспоминания и текущее внутреннее состояние Жильберты:\n\n"
        + memory_context +
        "\n\nИНСТРУКЦИЯ ДЛЯ ОТВЕТА:\n"
        "1. Отвечай по-новому каждый раз.\n"
        "2. Обязательно используй свои реальные убеждения из раздела 'Мои устоявшиеся убеждения'.\n"
        "3. Не повторяй одни и те же формулировки.\n"
        "4. Никаких личных примеров про пользователя."
    })

    print("\n===== CHAT MESSAGES =====\n")
    for i, msg in enumerate(chat_messages):
        print(f"{i}: {msg['role']}")
        print(msg["content"][:300])
        print("-" * 40)

    # LLM
    try:
        answer = llm_chat(chat_messages)
        logger.info(f"Ответ ИИ: {answer[:100]!r}")
    except LLMError as e:
        logger.error(f"Ошибка LLM: {e}")
        print(f"\n[ОШИБКА LLM] {e}")
        print("Пропускаю этот запрос. Попробуй ещё раз.\n")
        messages.pop()
        return

    print(f"\nИИ: {answer}\n")
    messages.append({"role": "assistant", "content": answer})
    save_memory(messages[1:])

    # Рефлексия каждые 25
    if message_counter % 25 == 0:
        logger.info("Триггер рефлексии")
        print("[REFLECTION TRIGGERED]")
        recent_messages = messages[-20:]
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


# ============ ГЛАВНЫЙ ЦИКЛ ============

def main():
    global saved_messages, message_counter, messages
    atexit.register(_save_on_exit)
    logger.info("Жильберта запущена.")

    print("\nЖильберта готова к разговору.")
    print("Команды: /knowledge, /teach, /reflect, /approve, /reject, /brain, /stats, выход\n")

    while True:
        try:
            user_text = input("Ты: ")
        except (KeyboardInterrupt, EOFError):
            print("\n")
            logger.info("Ctrl+C")
            break

        if user_text.lower() == "выход":
            logger.info("Выход")
            break

        if user_text == "/knowledge":
            cmd_knowledge()
        elif user_text.startswith("/teach "):
            cmd_teach(user_text[7:].strip())
        elif user_text.startswith("/reflect "):
            cmd_reflect(user_text[9:].strip())
        elif user_text == "/approve":
            cmd_approve()
        elif user_text == "/reject":
            cmd_reject()
        elif user_text.startswith("/knowledge "):
            cmd_knowledge_detail(user_text[11:].strip())
        elif user_text == "/brain":
            cmd_brain()
        elif user_text == "/stats":
            cmd_stats()
        else:
            cmd_chat(user_text)


if __name__ == "__main__":
    main()