import json
import os

FILE = "memory/curiosity.json"


def load_curiosity():

    if not os.path.exists(FILE):
        return []

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_curiosity(data):

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def add_curiosity(topic, reason):

    curiosity = load_curiosity()

    for item in curiosity:

        if item["topic"].lower() == topic.lower():
            return

    curiosity.append(
        {
            "topic": topic,
            "reason": reason
        }
    )

    save_curiosity(curiosity)