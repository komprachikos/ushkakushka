from brain.curiosity import generate_curiosity
from brain.reflection import generate_reflection

from core.curiosity import add_curiosity
from core.journal import add_thought
from core.logger import logger
from core.pipeline_state import PipelineState
from core.profile_memory import consolidate_facts

from config import (
    REFLECTION_INTERVAL,
    THOUGHT_MAX_LEN,
)


def run_reflection(state: PipelineState) -> None:
    """
    Выполняет периодическую рефлексию модели.
    """

    state.reflection = None
    state.curiosity = None

    if state.message_counter % REFLECTION_INTERVAL != 0:
        return

    logger.info("Триггер рефлексии")

    consolidate_facts()

    conversation_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in state.local_messages[-20:]
    )

    thought = generate_reflection(conversation_text)

    logger.debug("Рефлексия: %r", thought)

    if thought != "NONE" and len(thought) < THOUGHT_MAX_LEN:
        add_thought(thought)
        state.reflection = thought

        logger.info("Мысль: %s", thought)

    curiosity = generate_curiosity(conversation_text)

    if curiosity:
        add_curiosity(
            curiosity["topic"],
            curiosity["reason"],
        )

        state.curiosity = curiosity

        logger.info(
            "Любопытство: %s",
            curiosity["topic"],
        )