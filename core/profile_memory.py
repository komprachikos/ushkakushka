import json
from pathlib import Path
from core.atomic_json import safe_json_load, atomic_json_write
from core.paths import DATA_DIR
from core.llm_client import llm_chat, LLMError

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


def consolidate_facts():
    """Раз в N сообщений чистит профиль: убирает дубли, противоречия, устаревшее."""
    profile = load_profile()
    facts = profile.get("facts", [])
    if len(facts) < 3:
        return

    facts_text = "\n".join(f"• {f}" for f in facts)
    messages = [
        {
            "role": "system",
            "content": "Ты редактор фактов. У тебя список фактов о пользователе. Убери дубли, разреши противоречия (оставь самый свежий по смыслу), удали устаревшее. Верни только список фактов, по одному на строку, без пояснений."
        },
        {
            "role": "user",
            "content": f"Исходные факты:\n{facts_text}\n\nОчищенные факты (максимум 10):"
        }
    ]

    try:
        result = llm_chat(messages)
        new_facts = [line.strip("-• ").strip() for line in result.splitlines() if line.strip()]
        if new_facts:
            profile["facts"] = new_facts[:10]
            save_profile(profile)
    except LLMError:
        pass