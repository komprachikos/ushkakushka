from brain.recall import recall_memories
from mind.context_builder import build_internal_thought
from mind.associations import get_related_topics
from core.knowledge import get_knowledge
from core.journal import get_recent_thoughts
from core.curiosity import load_curiosity


def build_current_state(user_text, conflict_topic=None):
    memories = recall_memories(user_text)

    state = {
        "focus": None,
        "beliefs": [],
        "thoughts": []
    }

    if memories["knowledge"]:
        # Основной фокус
        main_topic = memories["knowledge"][0]
        state["focus"] = main_topic["topic"]

        # Добавляем убеждения
        for item in memories["knowledge"]:
            opinions = item.get("opinions", [])
            if not opinions:
                continue
            state["beliefs"].append({
                "topic": item["topic"],
                "summary": item.get("summary", ""),
                "opinion": opinions[-1]["text"]
            })

        # Основная внутренняя мысль
        thought = build_internal_thought(state["focus"])
        if thought:
            state["thoughts"].append(thought)

        # Добавляем связанные темы через related
        related_items = get_related_topics(state["focus"])

        for rel in related_items[:2]:
            knowledge = get_knowledge(rel["topic"])
            if knowledge is None:
                continue
            opinions = knowledge.get("opinions", [])
            if not opinions:
                continue
            state["thoughts"].append({
                "topic": knowledge["topic"],
                "reason": rel.get("via", "ассоциация"),
                "opinion": opinions[-1]["text"]
            })

    # Замыкаем рефлексию и любопытство
    from core.journal import get_recent_thoughts
    from core.curiosity import load_curiosity

    recent_reflections = get_recent_thoughts(2)
    if recent_reflections:
        state["recent_reflections"] = recent_reflections

    curiosity_list = load_curiosity()
    if curiosity_list:
        state["active_curiosity"] = curiosity_list[0]

    # АВТО-КОНФЛИКТ — теперь здесь, до render_state
    if conflict_topic:
        state["conflict_topic"] = conflict_topic

    return state