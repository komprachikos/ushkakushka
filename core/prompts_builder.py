from core.profile_memory import load_profile
from core.paths import PROMPTS_DIR

_personality_text = None

def _load_personality():
    global _personality_text
    if _personality_text is None:
        with open(PROMPTS_DIR / "personality.txt", "r", encoding="utf-8") as fh:
            _personality_text = fh.read()
    return _personality_text

def build_system_prompt():
    personality = _load_personality()
    profile = load_profile()
    facts = profile.get("facts", [])
    facts_text = "\n".join(f"• {fact}" for fact in facts) if facts else "• (пока нет фактов)"

    profile_text = f"""Информация о пользователе:

Имя: {profile.get('name', 'неизвестно')}
Факты:
{facts_text}
"""

    return personality + "\n\n" + profile_text