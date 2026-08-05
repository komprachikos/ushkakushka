from brain.fact_extractor import extract_fact
from core.logger import logger
from core.pipeline_state import PipelineState
from core.profile_memory import add_fact
from core.prompts_builder import build_system_prompt


def process_user_message(state: PipelineState) -> None:
    """
    Обрабатывает новое сообщение пользователя.

    - извлекает новые факты о пользователе;
    - обновляет system prompt при необходимости;
    - добавляет сообщение пользователя в историю.
    """

    fact = extract_fact(state.user_text)

    logger.debug("Факт: %r", fact)

    if fact != "NONE":
        add_fact(fact)

        state.local_messages[0] = {
            "role": "system",
            "content": build_system_prompt(),
        }

        logger.info("Новый факт: %s", fact)

    state.local_messages.append({
        "role": "user",
        "content": state.user_text,
    })