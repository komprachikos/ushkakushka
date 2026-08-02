import json
from pathlib import Path
from core.atomic_json import safe_json_load, atomic_json_write
from core.paths import DATA_DIR

PROFILE_FILE = DATA_DIR / "user_profile.json"


def load_profile():
    return safe_json_load(PROFILE_FILE, default={"name": "", "facts": []})


def save_profile(profile):
    atomic_json_write(PROFILE_FILE, profile)


def add_fact(fact):
    profile = load_profile()
    normalized_new = normalize_fact(fact)
    existing = {normalize_fact(item) for item in profile.get("facts", [])}
    if normalized_new not in existing:
        profile.setdefault("facts", []).append(fact)
        save_profile(profile)


def normalize_fact(text):
    return text.lower().strip().replace(".", "")
