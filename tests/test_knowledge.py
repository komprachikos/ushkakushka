from core.knowledge import (
    add_knowledge,
    get_knowledge
)

add_knowledge(
    topic="Великий фильтр",
    summary="Одна из гипотез парадокса Ферми.",
    opinion="Версия о саморазрушении цивилизаций кажется наиболее вероятной."
)

add_knowledge(
    topic="Великий фильтр",
    summary="Одна из гипотез парадокса Ферми.",
    opinion="После размышлений я считаю, что версия редкости разумной жизни выглядит убедительно."
)

print(
    get_knowledge("великий фильтр")
)


from core.knowledge import get_current_opinion

print()
print("CURRENT:")
print(
    get_current_opinion(
        "великий фильтр"
    )
)


from core.knowledge import get_topics

print()
print("TOPICS:")
print(get_topics())