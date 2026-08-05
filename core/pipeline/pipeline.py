from core.pipeline_state import PipelineState
from core.pipeline.base import Stage


class Pipeline:
    """Последовательно выполняет этапы обработки сообщения."""

    def __init__(self, stages: list[Stage]):
        self._stages = tuple(stages)

    def run(self, state: PipelineState) -> PipelineState:
        for stage in self._stages:
            stage.run(state)

        return state