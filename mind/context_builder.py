from core.knowledge import get_knowledge
from mind.thoughts import get_random_association

def build_internal_thought(topic):
    association = get_random_association(topic)

    if association is None:
        return None

    knowledge = get_knowledge(
        association["topic"]
    )

    if knowledge is None:
        return None

    opinions = knowledge.get("opinions", [])
    if not opinions:
        return None

    return {
        "topic": knowledge["topic"],
        "reason": association["via"],
        "opinion": opinions[-1]["text"]
    }