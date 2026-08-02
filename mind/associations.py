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

    related = set(x.lower() for x in current.get("related", []))
    result = []

    for item in knowledge:
        if item["topic"] == current["topic"]:
            continue
        for tag in item.get("related", []):
            if tag.lower() in related:
                result.append({"topic": item["topic"], "via": tag})
                break

    return result


def find_related_topics(topic):
    """Возвращает список кортежей (topic_name, overlap_count) отсортированных по релевантности."""
    related = set(r.lower() for r in _get_related_raw(topic))
    if not related:
        return []

    result = []
    for item in load_knowledge():
        if item["topic"].lower() == topic.lower():
            continue
        item_related = set(r.lower() for r in item.get("related", []))
        common = related & item_related
        if common:
            result.append((item["topic"], len(common)))

    result.sort(key=lambda x: x[1], reverse=True)
    return result


def _get_related_raw(topic):
    """Внутренний хелпер — получает related теги темы."""
    for item in load_knowledge():
        if item["topic"].lower() == topic.lower():
            return item.get("related", [])
    return []