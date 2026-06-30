from core.knowledge import get_knowledge
from mind.thoughts import get_random_association


def build_internal_context(
    topic,
    memory_context
):

    association = get_random_association(topic)

    if association is None:
        return memory_context

    knowledge = get_knowledge(
        association["topic"]
    )

    if knowledge is None:
        return memory_context

    opinion = knowledge["opinions"][-1]["text"]

    memory_context += f"""

Во время разговора тебе неожиданно вспомнилась другая тема.

ТЕМА:
{knowledge["topic"]}

Почему вспомнилась:
общая идея — {association["via"]}

Твое мнение по этой теме:

{opinion}

Это просто мысль.

Не обязательно рассказывать о ней пользователю.

Но если связь кажется естественной —
можешь кратко упомянуть её.
"""

    return memory_context


def build_internal_thought(topic):

    association = get_random_association(topic)

    if association is None:
        return None

    knowledge = get_knowledge(
        association["topic"]
    )

    if knowledge is None:
        return None

    return {
        "topic": knowledge["topic"],
        "reason": association["via"],
        "opinion": knowledge["opinions"][-1]["text"]
    }