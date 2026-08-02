from core.paths import MEMORY_DIR
from core.atomic_json import safe_json_load, atomic_json_write

FILE = MEMORY_DIR / "pending_study.json"


def load_pending():
    return safe_json_load(FILE, default={})


def save_pending(data):
    atomic_json_write(FILE, data)


def set_pending(topic, summary, opinion, related=None):
    save_pending({
        "topic": topic,
        "summary": summary,
        "opinion": opinion,
        "related": related or []
    })


def clear_pending():
    save_pending({})