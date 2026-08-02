from core.profile_memory import load_profile


def build_system_prompt():
    with open("prompts/personality.txt", "r", encoding="utf-8") as fh:
        personality = fh.read()

    profile = load_profile()
    facts = profile.get("facts", [])
    facts_text = "\n".join(f"• {fact}" for fact in facts) if facts else "• (пока нет фактов)"

    profile_text = f"""Информация о пользователе:

Имя: {profile.get('name', 'неизвестно')}
Факты:
{facts_text}
"""

    return personality + "\n\n" + profile_text
