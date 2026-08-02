from core.profile_memory import load_profile
from core.journal import get_recent_thoughts, load_journal


def handle_brain(session):
    profile = load_profile()
    print("\n=== PROFILE ===")
    print(f"Имя: {profile['name']}")
    print("\n=== FACTS ===")
    for fact in profile.get("facts", [])[-5:]:
        print(f"- {fact}")
    print("\n=== THOUGHTS ===")
    thoughts = get_recent_thoughts()
    for item in thoughts:
        print(f"- {item['thought']}")
    print()
    return True


def handle_stats(session):
    profile = load_profile()
    journal = load_journal()
    print("\n=== STATS ===")
    print(f"Сообщений: {len(session.saved_messages)}")
    print(f"Фактов: {len(profile.get('facts', []))}")
    print(f"Размышлений: {len(journal)}")
    if profile.get("facts"):
        print(f"\nПоследний факт:\n{profile['facts'][-1]}")
    if journal:
        print(f"\nПоследнее размышление:\n{journal[-1]['thought']}")
    print()
    return True