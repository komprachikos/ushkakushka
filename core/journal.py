import json
from pathlib import Path
from datetime import datetime

JOURNAL_FILE = Path("data/journal.json")

def add_thought(thought):
    entries = load_journal()

    entries.append(
        {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "thought": thought
        }
    )

    save_journal(entries)

def get_recent_thoughts(limit=5):
    entries = load_journal()

    return entries[-limit:]

def load_journal():
    try:
        with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_journal(entries):
    with open(JOURNAL_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)