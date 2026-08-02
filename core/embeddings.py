import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from core.atomic_json import safe_json_load, atomic_json_write
from core.knowledge import load_knowledge

EMBEDDINGS_FILE = Path("data/embeddings.json")
MODEL_NAME = "all-MiniLM-L6-v2"

# Кэшируем модель на уровне модуля — загружается один раз за процесс
_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def _load_embeddings():
    return safe_json_load(EMBEDDINGS_FILE, default={})


def _save_embeddings(data):
    atomic_json_write(EMBEDDINGS_FILE, data)


def get_embedding(text):
    model = _get_model()
    return model.encode(text).tolist()


def ensure_topic_embedding(topic):
    """Генерирует и сохраняет эмбеддинг для темы, если его ещё нет."""
    embeddings = _load_embeddings()
    if topic in embeddings:
        return embeddings[topic]
    embedding = get_embedding(topic)
    embeddings[topic] = embedding
    _save_embeddings(embeddings)
    return embedding


def ensure_all_embeddings():
    """Генерирует эмбеддинги для всех тем из knowledge.json."""
    knowledge = load_knowledge()
    for item in knowledge:
        ensure_topic_embedding(item["topic"])


def find_similar_topics(query, top_k=5, threshold=0.25):
    """
    Находит топ-K тем, ближайших к запросу по смыслу.
    Возвращает список кортежей (topic_name, similarity_score).
    """
    query_emb = np.array(get_embedding(query))
    embeddings = _load_embeddings()

    if not embeddings:
        return []

    topics = list(embeddings.keys())
    vectors = np.array([embeddings[t] for t in topics])

    # Нормализация и косинусное сходство
    query_norm = query_emb / np.linalg.norm(query_emb)
    vectors_norm = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    similarities = np.dot(vectors_norm, query_norm)

    top_indices = np.argsort(similarities)[::-1][:top_k]
    results = [(topics[i], float(similarities[i])) for i in top_indices]

    # Фильтруем по порогу
    return [(t, s) for t, s in results if s >= threshold]