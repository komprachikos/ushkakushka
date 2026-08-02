from core.knowledge import get_topics, get_knowledge, get_current_opinion


def handle_knowledge(session):
    print("\n=== KNOWLEDGE ===\n")
    topics = get_topics()
    if not topics:
        print("Пока нет сохранённых знаний.\n")
    else:
        for topic in topics:
            print(f"- {topic}")
        print()
    return True


def handle_knowledge_detail(session, topic):
    knowledge = get_knowledge(topic)
    if knowledge is None:
        print("\nТема не найдена.\n")
        return True
    print("\n=== KNOWLEDGE ===\n")
    print(f"Тема: {knowledge['topic']}")
    print(f"\nОписание:\n{knowledge['summary']}")
    opinion = get_current_opinion(topic)
    if opinion:
        print(f"\nТекущее мнение:\n{opinion['text']}")
    print(f"\nВерсий мнения: {len(knowledge.get('opinions', []))}")
    print("\nИстория:")
    for opinion in knowledge.get("opinions", []):
        print(f"- {opinion['date']} | {opinion['text']}")
    print()
    print()
    return True