import json
from pathlib import Path
from datetime import datetime
import random

KNOWLEDGE_FILE = Path("data/knowledge.json")


def load_knowledge():

    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except:
        return []


def save_knowledge(data):

    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def add_knowledge(
    topic,
    summary,
    opinion,
    related=None
):

    knowledge = load_knowledge()

    for item in knowledge:

        if item["topic"].lower() == topic.lower():

            item["summary"] = summary

            last_opinion = item["opinions"][-1]["text"]

            if last_opinion == opinion:
                return

            item["opinions"].append(
                {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "text": opinion
                }
            )

            item["related"] = related or item.get("related", [])

            save_knowledge(knowledge)
            return

    knowledge.append(
        {
            "topic": topic,
            "summary": summary,
            "related": related or [],
            "opinions": [
                {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "text": opinion
                }
            ],
            "reflections": []
        }
    )

    save_knowledge(knowledge)


def get_knowledge(topic):

    knowledge = load_knowledge()

    topic = topic.lower().strip()

    for item in knowledge:

        if item["topic"].lower() == topic:
            return item

    return None


def get_current_opinion(topic):

    item = get_knowledge(topic)

    if item is None:
        return None

    return item["opinions"][-1]


def has_knowledge(topic):

    return get_knowledge(topic) is not None


def get_topics():

    knowledge = load_knowledge()

    return [
        item["topic"]
        for item in knowledge
    ]


def get_random_topic(exclude=None):

    knowledge = load_knowledge()

    if exclude:

        knowledge = [
            item
            for item in knowledge
            if item["topic"].lower() != exclude.lower()
        ]

    if not knowledge:
        return None

    return random.choice(knowledge)


def add_reflection(topic, reflection):

    knowledge = load_knowledge()

    for item in knowledge:

        if item["topic"].lower() == topic.lower():

            if "reflections" not in item:
                item["reflections"] = []

            item["reflections"].append(
                {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "text": reflection
                }
            )

            save_knowledge(knowledge)
            return
        

def get_reflections(topic):

    item = get_knowledge(topic)

    if item is None:
        return []

    return item.get("reflections", [])


def get_related(topic):

    knowledge = get_knowledge(topic)

    print(knowledge)

    if knowledge is None:
        return []

    return knowledge.get("related", [])