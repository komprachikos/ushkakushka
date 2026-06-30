import random

from mind.associations import get_related_topics


def get_random_association(topic):

    related = get_related_topics(topic)

    if not related:
        return None

    return random.choice(related)