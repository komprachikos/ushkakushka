from abc import ABC, abstractmethod

from core.pipeline_state import PipelineState


class Stage(ABC):
    """Базовый класс этапа Pipeline."""

    @abstractmethod
    def run(self, state: PipelineState) -> None:
        """
        Выполняет этап обработки.

        Метод изменяет PipelineState и не возвращает значение.
        """
        raise NotImplementedError