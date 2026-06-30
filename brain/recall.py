from core.knowledge import get_topics, get_knowledge
from ollama import chat
from config import MODEL


def find_related_topics(user_text):

    topics = get_topics()

    if not topics:
        return []

    topics_text = "\n".join(topics)

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"""
Ты анализатор памяти.

Сообщение пользователя:

{user_text}

Из списка тем:

{topics_text}

Выбери темы, которые относятся к сообщению.

Если подходящих нет:

NONE

Если есть:

Верни только названия тем.
По одной на строку.
"""
            }
        ]
    )

    result = response.message.content.strip()

    if result == "NONE":
        return []

    return [
        line.strip()
        for line in result.splitlines()
        if line.strip()
    ]


def recall_memories(user_text):

    memories = {
        "facts": [],
        "thoughts": [],
        "knowledge": []
    }

    topics = find_related_topics(user_text)

    for topic in topics:

        knowledge = get_knowledge(topic)

        if knowledge:

            memories["knowledge"].append(
                knowledge
            )

    return memories


def build_memory_context(memories):

    parts = []

    if memories["knowledge"]:

        parts.append(
            "Жильберта вспомнила свои прошлые размышления."
        )

        for item in memories["knowledge"]:

            if not item["opinions"]:
                continue

            current_opinion = item["opinions"][-1]["text"]

            parts.append(
                f"""
Это воспоминание Жильберты.

Раньше она уже долго размышляла об этой теме.

ТЕМА:
{item['topic']}

Краткое описание:

{item['summary']}

После всех своих размышлений она пришла к следующему мнению:

{current_opinion}

Это мнение уже стало частью её взглядов.

Если во время разговора возникает эта тема,
Жильберта сначала вспоминает именно это мнение,
а затем уже может дополнить его новыми мыслями,
если для этого действительно появились основания.

Иначе она просто отвечает так,
как человек, который уже давно сформировал своё мнение.
"""
            )

    return "\n".join(parts)