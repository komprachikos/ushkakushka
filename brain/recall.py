from core.knowledge import get_knowledge
from core.llm_client import llm_chat, LLMError
from core.embeddings import find_similar_topics
from config import SIMILARITY_THRESHOLD

def find_related_topics(user_text):
    """
    Семантический поиск: находит темы, ближайшие к запросу по смыслу.
    Fallback на LLM, если эмбеддингов ещё нет (первый запуск).
    """
    results = find_similar_topics(user_text, top_k=5, threshold=SIMILARITY_THRESHOLD)
    if results:
        return [topic for topic, score in results]

    # Fallback: если ничего не нашли, спрашиваем LLM
    from core.knowledge import get_topics
    topics = get_topics()
    if not topics:
        return []

    topics_text = "\n".join(topics)

    messages = [
        {
            "role": "system",
            "content": """Ты Жильберта, женского рода. Ты анализатор памяти.

Тебе дан список тем из долгосрочной памяти.

Выбери темы, которые относятся к сообщению пользователя.

Если подходящих нет — ответь: NONE
Если есть — верни только названия тем, по одной на строку."""
        },
        {
            "role": "user",
            "content": f"Сообщение пользователя:\n{user_text}\n\nСписок тем:\n{topics_text}"
        }
    ]

    try:
        result = llm_chat(messages)
    except LLMError:
        return []

    if result == "NONE":
        return []

    return [
        line.strip()
        for line in result.splitlines()
        if line.strip()
    ]

def recall_memories(user_text):
    memories = {
        "facts": [],
        "thoughts": [],
        "knowledge": []
    }

    topics = find_related_topics(user_text)

    for topic in topics:
        knowledge = get_knowledge(topic)
        if knowledge:
            memories["knowledge"].append(knowledge)

    return memories