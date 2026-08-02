from ollama import chat
from config import MODEL, TEMPERATURE


class LLMError(Exception):
    pass


def llm_chat(messages, temperature=None):
    if temperature is None:
        temperature = TEMPERATURE
    try:
        response = chat(
            model=MODEL,
            messages=messages,
            options={"temperature": temperature}
        )
    except Exception as e:
        raise LLMError(f"Ollama error (model={MODEL}): {e}")

    if not response or not response.message or not response.message.content:
        raise LLMError("Empty response from model")

    return response.message.content.strip()