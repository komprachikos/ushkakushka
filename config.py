import os

# LLM
MODEL = os.getenv("MODEL", "qwen3:8b")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "10"))

# Рефлексия
REFLECTION_INTERVAL = int(os.getenv("REFLECTION_INTERVAL", "25"))
THOUGHT_MAX_LEN = int(os.getenv("THOUGHT_MAX_LEN", "180"))

# Эмбеддинги
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.25"))
TOP_K_SIMILAR = int(os.getenv("TOP_K_SIMILAR", "5"))