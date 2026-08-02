from pathlib import Path
from core.atomic_json import safe_json_load, atomic_json_write
from config import MAX_HISTORY
from core.paths import DATA_DIR

MEMORY_FILE = DATA_DIR / "memory.json"


def load_memory():
    return safe_json_load(MEMORY_FILE, default=[])


def save_memory(messages):
    # Сохраняем только последние MAX_HISTORY сообщений
    atomic_json_write(MEMORY_FILE, messages[-MAX_HISTORY:])