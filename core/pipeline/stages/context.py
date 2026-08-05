from core.pipeline.base import Stage
from core.pipeline_state import PipelineState
from core.context_builder import build_context


class ContextStage(Stage):
    """
    Формирует контекст для генерации ответа.
    """

    def run(self, state: PipelineState) -> None:
        state.context = build_context(
            state.local_messages,
            state.user_text,
            state.conflict_topic,
        )