from core.chat_builder import build_chat_messages
from core.conversation_context import ConversationContext
from core.prompt_context import build_full_system_prompt

from mind.current_state import build_current_state
from mind.state_prompt import render_state


def build_context(
    local_messages,
    user_text,
    conflict_topic,
) -> ConversationContext:
    """
    Строит полный контекст диалога для генерации ответа.
    """

    state = build_current_state(
        user_text,
        conflict_topic=conflict_topic,
    )

    memory_context = render_state(state)

    system_prompt = build_full_system_prompt(
        local_messages[0]["content"],
        memory_context,
    )

    chat_messages = build_chat_messages(
        system_prompt,
        local_messages,
    )

    return ConversationContext(
        state=state,
        memory_context=memory_context,
        system_prompt=system_prompt,
        chat_messages=chat_messages,
    )