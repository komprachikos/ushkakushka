from pathlib import Path
from core.atomic_json import safe_json_load, atomic_json_write

MEMORY_FILE = Path("data/memory.json")


def load_memory():
    return safe_json_load(MEMORY_FILE, default=[])


def save_memory(messages):
    atomic_json_write(MEMORY_FILE, messages)
