import json
import os

FILE = "memory/pending_study.json"


def load_pending():
    if not os.path.exists(FILE):
        return {}
    try:
        with open(FILE, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return {}


def save_pending(data):
    tmp = FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, FILE)


def set_pending(topic, summary, opinion, related=None):
    save_pending({
        "topic": topic,
        "summary": summary,
        "opinion": opinion,
        "related": related or []
    })


def clear_pending():
    save_pending({})
