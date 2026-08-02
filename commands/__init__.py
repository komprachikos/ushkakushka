"""Диспетчер команд."""
from core.logger import logger
from .knowledge_cmd import handle_knowledge, handle_knowledge_detail
from .teach_cmd import handle_teach, handle_approve, handle_reject
from .reflect_cmd import handle_reflect
from .brain_cmd import handle_brain, handle_stats
from .chat_cmd import handle_chat


def dispatch(session, user_text):
    logger.debug(f"Dispatch: {user_text[:50]!r}")

    if user_text.lower() == "выход":
        logger.info("Команда: выход")
        return False

    if user_text == "/knowledge":
        return handle_knowledge(session)
    if user_text.startswith("/knowledge "):
        return handle_knowledge_detail(session, user_text[11:].strip())
    if user_text.startswith("/teach "):
        return handle_teach(session, user_text[7:].strip())
    if user_text == "/approve":
        return handle_approve(session)
    if user_text == "/reject":
        return handle_reject(session)
    if user_text.startswith("/reflect "):
        return handle_reflect(session, user_text[9:].strip())
    if user_text == "/brain":
        return handle_brain(session)
    if user_text == "/stats":
        return handle_stats(session)

    return handle_chat(session, user_text)