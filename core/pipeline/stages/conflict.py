from core.pipeline.base import Stage
from core.pipeline_state import PipelineState
from core.conflict_detector import detect_conflict


class ConflictStage(Stage):
    """
    Определяет, противоречит ли текущее сообщение
    существующим убеждениям модели.
    """

    def run(self, state: PipelineState) -> None:
        recent_user_text = "\n".join(
            m["content"]
            for m in state.local_messages[-10:]
            if m["role"] == "user"
        )

        state.conflict_topic = detect_conflict(recent_user_text)