from core.pipeline.base import Stage
from core.pipeline_state import PipelineState
from core.reflection_runner import run_reflection


class ReflectionStage(Stage):
    """
    Запускает периодическую рефлексию модели.
    """

    def run(self, state: PipelineState) -> None:
        run_reflection(state)