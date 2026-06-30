import json
from pathlib import Path


PROFILE_FILE = Path("data/user_profile.json")

def load_profile():
    try:
        with open(PROFILE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {
            "name": "",
            "facts": []
        }
    
def save_profile(profile):
    with open(PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)

def add_fact(fact):
    profile = load_profile()

    normalized_new = normalize_fact(fact)

    existing = {
        normalize_fact(item)
        for item in profile["facts"]
    }

    if normalized_new not in existing:
        profile["facts"].append(fact)

    save_profile(profile)

def normalize_fact(text):
    return text.lower().strip().replace(".", "")