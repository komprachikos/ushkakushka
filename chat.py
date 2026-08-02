import atexit
from core.logger import logger
from core.session import ChatSession
from core.embeddings import rebuild_index
from commands import dispatch


def main():
    rebuild_index()

    session = ChatSession()
    atexit.register(session.save)

    logger.info("Жильберта готова к работе.")
    print("\nЖильберта готова к работе. Напиши что-нибудь.")
    print("Команды: /knowledge, /teach, /reflect, /approve, /reject, /brain, /stats, выход\n")

    while True:
        try:
            user_text = input("Ты: ")
        except (KeyboardInterrupt, EOFError):
            print("\n")
            logger.info("Ctrl+C")
            break

        should_continue = dispatch(session, user_text)
        if not should_continue:
            logger.info("Выход из программы.")
            break


if __name__ == "__main__":
    main()