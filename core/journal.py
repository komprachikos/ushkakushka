from datetime import datetime
from pathlib import Path
from core.atomic_json import safe_json_load, atomic_json_write
from core.paths import DATA_DIR

JOURNAL_FILE = DATA_DIR / "journal.json"


def add_thought(thought):
    entries = load_journal()
    entries.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "thought": thought
    })
    save_journal(entries)


def get_recent_thoughts(limit=5):
    return load_journal()[-limit:]


def load_journal():
    return safe_json_load(JOURNAL_FILE, default=[])


def save_journal(entries):
    atomic_json_write(JOURNAL_FILE, entries)
