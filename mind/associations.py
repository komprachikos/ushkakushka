from core.knowledge import load_knowledge


def get_related_topics(topic):

    knowledge = load_knowledge()

    current = None

    for item in knowledge:

        if item["topic"].lower() == topic.lower():

            current = item
            break

    if current is None:
        return []

    related = set(
        x.lower()
        for x in current.get("related", [])
    )

    result = []

    for item in knowledge:

        if item["topic"] == current["topic"]:
            continue

        for tag in item.get("related", []):

            if tag.lower() in related:

                result.append(
                    {
                        "topic": item["topic"],
                        "via": tag
                    }
                )

                break

    return result