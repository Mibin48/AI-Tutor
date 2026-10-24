from typing import Any
from backend import config
from backend.rag.loader import load_documents
from backend.rag.chunker import chunk_documents

try:
    from langchain_community.vectorstores import FAISS
    from langchain_ollama import OllamaEmbeddings
except ImportError:
    FAISS = None  # type: ignore
    OllamaEmbeddings = None  # type: ignore


def get_vector_db(rebuild: bool = False) -> Any:
    """Build or load FAISS vector database from disk."""
    if not FAISS or not OllamaEmbeddings:
        return None

    embeddings = OllamaEmbeddings(model=config.EMBED_MODEL)

    if config.INDEX_DIR.exists() and not rebuild:
        return FAISS.load_local(
            str(config.INDEX_DIR), embeddings, allow_dangerous_deserialization=True
        )

    docs = load_documents(config.DATA_DIR)
    chunks = chunk_documents(docs)
    print(f"Indexed {len(docs)} document(s) into {len(chunks)} chunks")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(str(config.INDEX_DIR))
    return db
