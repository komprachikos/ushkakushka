from core.embeddings import find_similar_topics
from core.knowledge import (
    get_knowledge,
    get_topics,
)
from core.llm_client import LLMError, llm_chat

from config import (
    SIMILARITY_THRESHOLD,
    TOP_K_SIMILAR,
)


SYSTEM_PROMPT = """Ты Жильберта, женского рода. Ты анализатор памяти.

Тебе дан список тем из долгосрочной памяти.

Выбери темы, которые относятся к сообщению пользователя.

Если подходящих нет — ответь:

NONE

Если есть — верни только названия тем,
по одной теме на строку.
"""


def find_related_topics(user_text: str) -> list[str]:
    """
    Возвращает темы памяти, связанные с сообщением пользователя.
    Сначала используется поиск по эмбеддингам,
    затем — LLM как резервный вариант.
    """

    similar_topics = find_similar_topics(
        user_text,
        top_k=TOP_K_SIMILAR,
        threshold=SIMILARITY_THRESHOLD,
    )

    if similar_topics:
        return [
            topic
            for topic, _ in similar_topics
        ]

    topics = get_topics()

    if not topics:
        return []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": (
                f"Сообщение пользователя:\n{user_text}"
                f"\n\nСписок тем:\n"
                + "\n".join(topics)
            ),
        },
    ]

    try:
        result = llm_chat(messages).strip()

    except LLMError:
        return []

    if result == "NONE":
        return []

    return [
        line.strip()
        for line in result.splitlines()
        if line.strip()
    ]


def recall_memories(user_text: str) -> dict:
    """
    Возвращает релевантные воспоминания.
    """

    memories = {
        "facts": [],
        "thoughts": [],
        "knowledge": [],
    }

    for topic in find_related_topics(user_text):
        knowledge = get_knowledge(topic)

        if knowledge:
            memories["knowledge"].append(knowledge)

    return memories