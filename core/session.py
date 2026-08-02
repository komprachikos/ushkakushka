from core.memory import load_memory, save_memory
from core.prompts_builder import build_system_prompt
from core.logger import logger


class ChatSession:
    """Состояние сессии диалога."""

    def __init__(self):
        self.saved_messages = load_memory()
        self.message_counter = len(self.saved_messages)
        self.messages = [
            {"role": "system", "content": build_system_prompt()}
        ]
        self.messages.extend(self.saved_messages)
        logger.info(f"Сессия начата. Загружено {len(self.saved_messages)} сообщений.")

    def save(self):
        logger.info("Сохранение памяти перед выходом...")
        try:
            save_memory(self.messages[1:])
            logger.info("Память сохранена.")
        except Exception as e:
            logger.error(f"Ошибка сохранения: {e}")