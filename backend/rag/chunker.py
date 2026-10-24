from typing import Any
from backend import config

try:
    from langchain_text_splitters import (
        MarkdownHeaderTextSplitter,
        RecursiveCharacterTextSplitter,
    )
except ImportError:
    MarkdownHeaderTextSplitter = None  # type: ignore
    RecursiveCharacterTextSplitter = None  # type: ignore


def chunk_documents(docs: list[Any]) -> list[Any]:
    """Split documents by markdown headings, then by size with breadcrumbs."""
    if not MarkdownHeaderTextSplitter or not RecursiveCharacterTextSplitter:
        # Fallback simple chunking if text splitters not installed
        chunks = []
        for doc in docs:
            content = doc.page_content
            for i in range(0, len(content), config.CHUNK_SIZE - config.CHUNK_OVERLAP):
                slice_text = content[i : i + config.CHUNK_SIZE]
                chunks.append(type(doc)(page_content=slice_text, metadata=doc.metadata))
        return chunks

    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "chapter"), ("##", "section"), ("###", "subsection")],
        strip_headers=True,
    )
    size_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks: list[Any] = []
    for doc in docs:
        source = doc.metadata.get("source", "")
        if source.endswith(".md"):
            sections = header_splitter.split_text(doc.page_content)
            for s in sections:
                s.metadata["source"] = source
        else:
            sections = [doc]

        for chunk in size_splitter.split_documents(sections):
            crumbs = [
                chunk.metadata[k]
                for k in ("chapter", "section", "subsection")
                if k in chunk.metadata
            ]
            if crumbs:
                chunk.page_content = f"[{' > '.join(crumbs)}]\n{chunk.page_content}"
            chunks.append(chunk)

    return chunks
