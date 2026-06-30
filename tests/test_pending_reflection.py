from core.pending_reflection import (
    save_pending_reflection,
    load_pending_reflection,
    clear_pending_reflection
)

save_pending_reflection(
    {
        "topic": "Великий фильтр",
        "opinion": "Новое мнение"
    }
)

print(load_pending_reflection())

clear_pending_reflection()

print(load_pending_reflection())