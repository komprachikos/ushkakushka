from brain.recall import recall_memories
from mind.context_builder import build_internal_thought
from mind.associations import get_related_topics
from core.knowledge import get_knowledge


def build_current_state(user_text):
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
            state["beliefs"].append({
                "topic": item["topic"],
                "summary": item["summary"],
                "opinion": item["opinions"][-1]["text"]
            })

        # Основная внутренняя мысль
        thought = build_internal_thought(state["focus"])
        if thought:
            state["thoughts"].append(thought)

        # Добавляем связанные темы через related (это важно!)
        related_items = get_related_topics(state["focus"])
        
        for rel in related_items[:2]:  # берём максимум 2 связанные темы
            knowledge = get_knowledge(rel["topic"])
            if knowledge and knowledge["opinions"]:
                state["thoughts"].append({
                    "topic": knowledge["topic"],
                    "reason": rel["via"],
                    "opinion": knowledge["opinions"][-1]["text"]
                })

    return state