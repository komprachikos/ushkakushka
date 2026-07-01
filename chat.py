from ollama import chat

from config import MODEL

from core.memory import load_memory, save_memory

from core.profile_memory import load_profile, add_fact

from brain.fact_extractor import extract_fact

from brain.reflection import generate_reflection
from core.journal import add_thought, get_recent_thoughts, load_journal
from core.knowledge import (get_topics, get_knowledge, get_current_opinion, add_knowledge)

from brain.teacher import study_topic
from core.pending_study import set_pending,load_pending, clear_pending

from brain.reflection_on_topic import reflect_on_topic
from core.pending_reflection import save_pending_reflection, load_pending_reflection, clear_pending_reflection

from mind.context_builder import build_internal_context
from mind.current_state import build_current_state
from mind.state_prompt import render_state

import atexit
from brain.curiosity import generate_curiosity


with open("prompts/personality.txt", "r", encoding="utf-8") as f:
    personality = f.read()


def build_system_prompt():

    profile = load_profile()

    profile_text = f"""
Информация о пользователе:

Имя: {profile['name']}

Факты:
{chr(10).join(profile['facts'])}
"""

    return personality + "\n\n" + profile_text


saved_messages = load_memory()
message_counter = len(saved_messages)


messages = [
    {
        "role": "system",
        "content": build_system_prompt()
    }
]

messages.extend(saved_messages)


def save_on_exit():
    print("\n\n[ВЫХОД] Сохраняю память...")
    save_memory(messages[1:])
    print("Память сохранена.")

atexit.register(save_on_exit)


while True:
    user_text = input("Ты: ")


    if user_text.lower() == "выход":
        break


    if user_text == "/knowledge":

        print("\n=== KNOWLEDGE ===\n")

        topics = get_topics()

        if not topics:
            print("Пока нет сохранённых знаний.\n")

        else:
            for topic in topics:
                print(f"- {topic}")

            print()

        continue


    if user_text.startswith("/teach "):

        topic = user_text.replace(
            "/teach ",
            ""
        ).strip()

        result = study_topic(topic)

        set_pending(
            topic=topic,
            summary=result["summary"],
            opinion=result["opinion"],
            related=result["related"]
        )

        print("\n=== STUDY RESULT ===\n")

        print(f"Тема: {topic}")

        print(
            f"\nОписание:\n{result['summary']}"
        )

        print(
            f"\nПредварительное мнение:\n{result['opinion']}"
        )

        print("\nRELATED:")

        for item in result["related"]:
            print(f"- {item}")

        print(
            "\nСохранить знание: /approve"
        )

        print(
            "Отменить: /reject\n"
        )

        continue


    if user_text.startswith("/reflect "):

        topic = user_text.replace(
            "/reflect ",
            ""
        ).strip()

        knowledge = get_knowledge(topic)

        if knowledge is None:

            print("\nТема не найдена.\n")
            continue

        current_opinion = (
            knowledge["opinions"][-1]["text"]
        )

        result = reflect_on_topic(
            topic,
            knowledge["summary"],
            current_opinion
        )

        print("\n=== REFLECTION ===\n")

        print(f"Тема: {topic}")

        print(
            f"\nРазмышление:\n"
            f"{result['reflection']}"
        )

        print(
            f"\nНовое мнение:\n"
            f"{result['opinion']}"
        )

        save_pending_reflection(
            {
                "topic": topic,
                "summary": knowledge["summary"],
                "old_opinion": current_opinion,
                "new_opinion": result["opinion"],
                "related": knowledge.get("related", [])
            }
        )

        print(
            "\nСохранить: /approve\n"
            "Отменить: /reject\n"
        )

        continue


    if user_text == "/approve":

        pending_reflection = (
            load_pending_reflection()
        )

        if pending_reflection:

            old_opinion = (
                pending_reflection["old_opinion"]
                .strip()
            )

            new_opinion = (
                pending_reflection["new_opinion"]
                .strip()
            )

            if old_opinion == new_opinion:

                print(
                    "\nМнение не изменилось."
                    "\nНовая версия не сохранена.\n"
                )

                clear_pending_reflection()

                continue

            add_knowledge(
                topic=pending_reflection["topic"],
                summary=pending_reflection["summary"],
                opinion=pending_reflection["new_opinion"],
                related=pending_reflection["related"]
            )

            clear_pending_reflection()

            print(
                "\nНовая версия мнения сохранена.\n"
            )

            continue


        pending = load_pending()

        if not pending:

            print(
                "\nНет ожидающего знания.\n"
            )

            continue

        add_knowledge(
            topic=pending["topic"],
            summary=pending["summary"],
            opinion=pending["opinion"],
            related=pending["related"]
        )

        clear_pending()

        print(
            "\nЗнание сохранено.\n"
        )

        continue


    if user_text == "/reject":

        clear_pending()

        print(
            "\nИзучение отменено.\n"
        )

        continue


    if user_text.startswith("/knowledge "):

        topic = user_text.replace(
            "/knowledge ",
            ""
        ).strip()

        knowledge = get_knowledge(topic)

        if knowledge is None:

            print("\nТема не найдена.\n")
            continue

        print("\n=== KNOWLEDGE ===\n")

        print(
            f"Тема: {knowledge['topic']}"
        )

        print(
            f"\nОписание:\n{knowledge['summary']}"
        )

        opinion = get_current_opinion(topic)

        print(
            f"\nТекущее мнение:\n{opinion['text']}"
        )

        print(
            f"\nВерсий мнения: {len(knowledge['opinions'])}"
        )

        print("\nИстория:")

        for opinion in knowledge["opinions"]:

            print(
                f"- {opinion['date']} | {opinion['text']}"
        )

        print()

        print()

        continue


    if user_text == "/brain":

        profile = load_profile()

        print("\n=== PROFILE ===")
        print(f"Имя: {profile['name']}")

        print("\n=== FACTS ===")

        for fact in profile["facts"][-5:]:
            print(f"- {fact}")

        print("\n=== THOUGHTS ===")

        thoughts = get_recent_thoughts()

        for item in thoughts:
            print(f"- {item['thought']}")

        print()
        continue


    if user_text == "/stats":

        profile = load_profile()
        journal = load_journal()

        print("\n=== STATS ===")

        print(f"Сообщений: {len(saved_messages)}")
        print(f"Фактов: {len(profile['facts'])}")
        print(f"Размышлений: {len(journal)}")

        if profile["facts"]:
            print(
                f"\nПоследний факт:\n{profile['facts'][-1]}"
            )

        if journal:
            print(
                f"\nПоследнее размышление:\n{journal[-1]['thought']}"
            )

        print()
        continue


    fact = extract_fact(user_text)
    print(f"DEBUG FACT {repr(fact)}")

    if fact != "NONE":
        add_fact(fact)
        messages[0]["content"] = build_system_prompt()
        print("\n[PROFILE RELOADED]\n")
        print(f"\n[Новый факт] {fact}\n")


    messages.append({
        "role": "user",
        "content": user_text
    })

    message_counter += 1
    print(f"[MESSAGE COUNTER] {message_counter}")

    
    state = build_current_state(user_text)  ###

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
        })                               ###


    print("\n===== CHAT MESSAGES =====\n")

    for i, msg in enumerate(chat_messages):     #
        print(f"{i}: {msg['role']}")
        print(msg["content"][:300])
        print("-" * 40)


    try:
        response = chat(
            model=MODEL,
            messages=chat_messages
        )
    
        answer = response.message.content
    
        if not answer or not answer.strip():
            print("\n[ОШИБКА] Модель вернула пустой ответ. Пропускаю.\n")
            messages.pop()
            continue
        
    except Exception as e:
        print(f"\n[ОШИБКА LLM] {e}")
        print("Пропускаю этот запрос. Попробуй ещё раз.\n")
        messages.pop()
        continue

    print(f"\nИИ: {answer}\n")

    messages.append({
        "role": "assistant",
        "content": answer
    })

    save_memory(messages[1:])

    if message_counter % 25 == 0:

        print("[REFLECTION TRIGGERED]")

        recent_messages = messages[-20:]

        conversation_text = "\n".join(
            f"{msg['role']}: {msg['content']}"
            for msg in recent_messages
        )

        thought = generate_reflection(conversation_text)
        print(f"[DEBUG THOUGHT] {repr(thought)}")

        if thought != "NONE" and len(thought) < 180:
            add_thought(thought)
            print(f"\n[Размышление Жильберты] {thought}\n")

        curiosity = generate_curiosity(conversation_text)
        
        if curiosity:
            print(f"\n[Жильберта заинтересовалась]")
            print(f"Тема: {curiosity['topic']}")
            print(f"Причина: {curiosity['reason']}\n")
            print(f"Если хочешь, чтобы я изучила эту тему — напиши:")
            print(f"/teach {curiosity['topic']}")