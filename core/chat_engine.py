from core.pipeline.pipeline import Pipeline
from core.pipeline_state import PipelineState

from core.pipeline.stages.process_user import ProcessUserStage
from core.pipeline.stages.conflict import ConflictStage
from core.pipeline.stages.context import ContextStage
from core.pipeline.stages.generate import GenerateStage
from core.pipeline.stages.persist import PersistStage
from core.pipeline.stages.reflection import ReflectionStage


PIPELINE = Pipeline([
    ProcessUserStage(),
    ConflictStage(),
    ContextStage(),
    GenerateStage(),
    PersistStage(),
    ReflectionStage(),
])


def process_message(
    messages,
    user_text,
    message_counter=0,
):
    """
    Обрабатывает одно сообщение пользователя.

    Используется всеми интерфейсами (CLI, Streamlit и др.).
    """

    state = PipelineState(
        local_messages=list(messages),
        user_text=user_text,
        message_counter=message_counter,
    )

    PIPELINE.run(state)

    context = state.context

    return (
        state.answer,
        state.local_messages,
        context.state,
        context.memory_context,
        context.system_prompt,
        state.message_counter,
        state.reflection,
        state.curiosity,
    )