import json
from pathlib import Path
from core.atomic_json import safe_json_load, atomic_json_write
from core.paths import MEMORY_DIR

FILE = MEMORY_DIR / "pending_reflection.json"


def save_pending_reflection(data):
    atomic_json_write(FILE, data)


def load_pending_reflection():
    data = safe_json_load(FILE, default=None)
    if data == {}:
        return None
    return data


def clear_pending_reflection():
    if FILE.exists():
        FILE.unlink()
