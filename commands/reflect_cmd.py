from core.logger import logger
from core.knowledge import get_knowledge
from core.pending_reflection import save_pending_reflection
from brain.reflection_on_topic import reflect_on_topic


def handle_reflect(session, topic):
    logger.info(f"/reflect {topic}")
    from core.pending_study import clear_pending
    clear_pending()
    knowledge = get_knowledge(topic)
    if knowledge is None:
        print("\nТема не найдена.\n")
        return True
    if not knowledge.get("opinions"):
        print("\nПо этой теме ещё нет мнения.\n")
        return True

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
    return True