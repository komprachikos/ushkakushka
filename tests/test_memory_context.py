from brain.recall import (
    recall_memories,
    build_memory_context
)

memories = recall_memories(
    "Что ты думаешь о Великом фильтре?"
)

print(
    build_memory_context(memories)
)