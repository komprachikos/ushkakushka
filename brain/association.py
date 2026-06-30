from core.knowledge import (
    load_knowledge,
    get_related
)


def find_related_topics(topic):

    related = {
        r.lower()
        for r in get_related(topic)
    }

    if not related:
        return []

    result = []

    for item in load_knowledge():

        if item["topic"].lower() == topic.lower():
            continue

        item_related = {
            r.lower()
            for r in item.get("related", [])
        }

        common = related & item_related

        if common:

            result.append(
                (
                    item["topic"],
                    len(common)
                )
            )

    result.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return result