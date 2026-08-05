import numpy as np

from config import (
    SIMILARITY_THRESHOLD,
    TOP_K_SIMILAR,
)
from core.embeddings import (
    find_similar_topics,
    get_embedding,
)
from core.knowledge import get_current_opinion


COSINE_CONFLICT_THRESHOLD = 0.35


def detect_conflict(user_text: str) -> str | None:
    """
    Возвращает тему, если обнаружено противоречие
    между текущим сообщением и существующими убеждениями.
    """

    if not user_text:
        return None

    similar_topics = find_similar_topics(
        user_text,
        top_k=TOP_K_SIMILAR,
        threshold=SIMILARITY_THRESHOLD,
    )

    if not similar_topics:
        return None

    user_embedding = np.asarray(get_embedding(user_text))

    user_norm = np.linalg.norm(user_embedding)

    if user_norm == 0:
        return None

    for topic, _ in similar_topics:
        opinion = get_current_opinion(topic)

        if opinion is None:
            continue

        opinion_embedding = np.asarray(
            get_embedding(opinion["text"])
        )

        opinion_norm = np.linalg.norm(opinion_embedding)

        if opinion_norm == 0:
            continue

        cosine = float(
            np.dot(user_embedding, opinion_embedding)
            / (user_norm * opinion_norm)
        )

        if cosine < COSINE_CONFLICT_THRESHOLD:
            return topic

    return None