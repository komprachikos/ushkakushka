"""Единое логирование."""
import logging
import logging.handlers
from pathlib import Path

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("ushkakushka")
logger.setLevel(logging.DEBUG)

# INFO+ в chat.log
info_handler = logging.handlers.RotatingFileHandler(
    LOGS_DIR / "chat.log", maxBytes=1_000_000, backupCount=5, encoding="utf-8"
)
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)

# DEBUG+ в debug.log
debug_handler = logging.handlers.RotatingFileHandler(
    LOGS_DIR / "debug.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
)
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)

# Консоль
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logger.addHandler(info_handler)
logger.addHandler(debug_handler)
logger.addHandler(console)