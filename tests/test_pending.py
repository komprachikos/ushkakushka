from core.pending_study import (
    set_pending,
    load_pending
)

set_pending(
    topic="Великий фильтр",
    summary="Тестовое описание",
    opinion="Тестовое мнение"
)

print(
    load_pending()
)