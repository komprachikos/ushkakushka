from core.pipeline.base import Stage
from core.pipeline_state import PipelineState

from core.llm_client import llm_chat, LLMError
from core.logger import logger
from config import TEMPERATURE


class GenerateStage(Stage):
    """
    Генерирует ответ LLM.
    """

    def run(self, state: PipelineState) -> None:
        try:
            state.answer = llm_chat(
                state.context.chat_messages,
                temperature=TEMPERATURE,
            )

            logger.info("Ответ ИИ: %r", state.answer[:100])

        except LLMError:
            raise