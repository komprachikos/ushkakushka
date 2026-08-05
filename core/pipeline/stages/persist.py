from core.pipeline.base import Stage
from core.pipeline_state import PipelineState

from core.memory import save_memory
from core.logger import logger


class PersistStage(Stage):
    """
    Сохраняет ответ ассистента в историю
    и записывает обновлённую память.
    """

    def run(self, state: PipelineState) -> None:
        state.local_messages.append(
            {
                "role": "assistant",
                "content": state.answer,
            }
        )

        save_memory(state.local_messages[1:])

        logger.debug("Память сохранена")