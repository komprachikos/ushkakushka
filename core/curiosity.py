from pathlib import Path
from core.atomic_json import safe_json_load, atomic_json_write

FILE = Path("memory/curiosity.json")


def load_curiosity():
    return safe_json_load(FILE, default=[])


def save_curiosity(data):
    atomic_json_write(FILE, data)


def add_curiosity(topic, reason):
    curiosity = load_curiosity()
    for item in curiosity:
        if item["topic"].lower() == topic.lower():
            return
    curiosity.append({"topic": topic, "reason": reason})
    save_curiosity(curiosity)


def get_curiosity_list():
    return load_curiosity()


def remove_curiosity(topic):
    curiosity = load_curiosity()
    curiosity = [c for c in curiosity if c["topic"].lower() != topic.lower()]
    save_curiosity(curiosity)