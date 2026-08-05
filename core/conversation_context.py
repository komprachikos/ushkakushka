from dataclasses import dataclass


@dataclass
class ConversationContext:

    state: dict

    memory_context: str

    system_prompt: str

    chat_messages: list