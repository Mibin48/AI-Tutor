from typing import Any
from backend import config
from backend.rag.index import get_vector_db
from backend.rag.loader import load_documents
from backend.rag.chunker import chunk_documents


class FallbackRetriever:
    """Keyword search fallback over textbook chunks when Ollama is offline."""

    def __init__(self):
        self.chunks = []
        try:
            docs = load_documents(config.DATA_DIR)
            self.chunks = chunk_documents(docs)
        except Exception:
            pass

    def invoke(self, query: str) -> list[Any]:
        keywords = [w.lower() for w in query.split() if len(w) > 2]
        scored = []
        for c in self.chunks:
            text = c.page_content.lower()
            score = sum(1 for kw in keywords if kw in text)
            if score > 0:
                scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[: config.TOP_K]] or self.chunks[: config.TOP_K]


def get_retriever() -> Any:
    """Return MMR retriever if Ollama/FAISS is active, else FallbackRetriever."""
    try:
        db = get_vector_db()
        if db:
            return db.as_retriever(
                search_type="mmr",
                search_kwargs={"k": config.TOP_K, "fetch_k": 12},
            )
    except Exception as e:
        print(f"Notice: RAG index offline ({e}), using local text fallback.")
    return FallbackRetriever()


_active_retriever = None


def retrieve(question: str, history: list[tuple[str, str]] | None = None) -> list[Any]:
    """Retrieve top-K chunks for a question, prepending previous turn for follow-ups."""
    global _active_retriever
    if _active_retriever is None:
        _active_retriever = get_retriever()

    query = question
    if history:
        query = f"{history[-1][0]} {question}"

    try:
        return _active_retriever.invoke(query)
    except Exception as e:
        print(f"Retriever error ({e}), switching to fallback retriever.")
        _active_retriever = FallbackRetriever()
        return _active_retriever.invoke(query)
