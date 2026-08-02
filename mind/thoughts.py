import random

from mind.associations import get_related_topics


def get_random_association(topic):
    related = get_related_topics(topic)

    if not related:
        return None

    # Взвешенный случайный выбор: чем больше общих тегов, тем выше шанс
    weights = [r.get("overlap_count", 1) for r in related]
    return random.choices(related, weights=weights, k=1)[0]