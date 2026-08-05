from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class PipelineState:
    """
    Общее состояние обработки одного сообщения.
    Передается через весь Pipeline.
    """

    local_messages: list
    user_text: str
    message_counter: int

    conflict_topic: str |None = None

    context: Any | None = None

    answer: str | None = None

    reflection: str | None = None
    curiosity: dict | None = None