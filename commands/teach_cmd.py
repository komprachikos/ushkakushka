from core.logger import logger
from core.knowledge import add_knowledge
from core.pending_study import set_pending, load_pending, clear_pending
from core.pending_reflection import load_pending_reflection, clear_pending_reflection
from core.embeddings import ensure_topic_embedding
from brain.teacher import study_topic


def handle_teach(session, topic):
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
    return True


def handle_approve(session):
    # Сначала проверяем pending reflection
    pending_reflection = load_pending_reflection()
    if pending_reflection:
        old_opinion = pending_reflection.get("old_opinion", "").strip()
        new_opinion = pending_reflection.get("new_opinion", "").strip()
        if old_opinion == new_opinion:
            print("\nМнение не изменилось. Новая версия не сохранена.\n")
            clear_pending_reflection()
            return True
        add_knowledge(
            topic=pending_reflection["topic"],
            summary=pending_reflection["summary"],
            opinion=pending_reflection["new_opinion"],
            related=pending_reflection.get("related", [])
        )
        ensure_topic_embedding(pending_reflection["topic"])
        clear_pending_reflection()
        print("\nНовая версия мнения сохранена.\n")
        logger.info(f"Рефлексия сохранена: {pending_reflection['topic']}")
        return True

    # Потом проверяем pending study
    pending = load_pending()
    if not pending:
        print("\nНет ожидающих операций.\n")
        return True

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


def handle_reject(session):
    logger.info("/reject")
    clear_pending()
    print("\nИзучение отменено.\n")
    return True