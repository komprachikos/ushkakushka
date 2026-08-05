INSTRUCTION_BLOCK = (
    "ИНСТРУКЦИЯ ДЛЯ ОТВЕТА:\n"
    "1. Отвечай по-новому каждый раз.\n"
    "2. Обязательно используй свои реальные убеждения из раздела "
    "'Мои устоявшиеся убеждения'.\n"
    "3. Не повторяй одни и те же формулировки.\n"
    "4. Никаких личных примеров про пользователя."
)


def build_full_system_prompt(system_prompt: str, memory_context: str) -> str:
    return (
        system_prompt
        + "\n\n"
        + memory_context
        + "\n\n"
        + INSTRUCTION_BLOCK
    )