import random
from datetime import datetime
from pathlib import Path
from core.atomic_json import safe_json_load, atomic_json_write

KNOWLEDGE_FILE = Path("data/knowledge.json")


def load_knowledge():
    return safe_json_load(KNOWLEDGE_FILE, default=[])


def save_knowledge(data):
    atomic_json_write(KNOWLEDGE_FILE, data)


def add_knowledge(topic, summary, opinion, related=None):
    knowledge = load_knowledge()
    for item in knowledge:
        if item["topic"].lower() == topic.lower():
            item["summary"] = summary
            opinions = item.get("opinions", [])
            if opinions and opinions[-1]["text"] == opinion:
                return
            item.setdefault("opinions", []).append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "text": opinion
            })
            item["related"] = related or item.get("related", [])
            save_knowledge(knowledge)
            return

    knowledge.append({
        "topic": topic,
        "summary": summary,
        "related": related or [],
        "opinions": [{"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "text": opinion}],
        "reflections": []
    })
    save_knowledge(knowledge)


def get_knowledge(topic):
    topic = topic.lower().strip()
    for item in load_knowledge():
        if item["topic"].lower() == topic:
            return item
    return None


def get_current_opinion(topic):
    item = get_knowledge(topic)
    if item is None:
        return None
    opinions = item.get("opinions", [])
    if not opinions:
        return None
    return opinions[-1]


def has_knowledge(topic):
    return get_knowledge(topic) is not None


def get_topics():
    return [item["topic"] for item in load_knowledge()]


def get_random_topic(exclude=None):
    knowledge = load_knowledge()
    if exclude:
        knowledge = [item for item in knowledge if item["topic"].lower() != exclude.lower()]
    if not knowledge:
        return None
    return random.choice(knowledge)


def add_reflection(topic, reflection):
    knowledge = load_knowledge()
    for item in knowledge:
        if item["topic"].lower() == topic.lower():
            item.setdefault("reflections", []).append({
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "text": reflection
            })
            save_knowledge(knowledge)
            return


def get_reflections(topic):
    item = get_knowledge(topic)
    if item is None:
        return []
    return item.get("reflections", [])


def get_related(topic):
    item = get_knowledge(topic)
    if item is None:
        return []
    return item.get("related", [])
