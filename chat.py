import atexit
from core.logger import logger
from core.session import ChatSession
from commands import dispatch


def main():
    session = ChatSession()
    atexit.register(session.save)

    logger.info("Жильберта запущена.")
    print("\nЖильберта готова к разговору.")
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
            logger.info("Выход по команде.")
            break


if __name__ == "__main__":
    main()