from pathlib import Path
from typing import Any

try:
    from langchain_core.documents import Document
except ImportError:
    # Minimal fallback Document structure if langchain is not yet installed
    class Document:  # type: ignore
        def __init__(self, page_content: str, metadata: dict | None = None):
            self.page_content = page_content
            self.metadata = metadata or {}

try:
    from langchain_community.document_loaders import PyPDFLoader
except ImportError:
    PyPDFLoader = None  # type: ignore

try:
    import pypdf
except ImportError:
    pypdf = None


def load_documents(data_dir: Path) -> list[Any]:
    """Load markdown files first; fall back to PDF only if no .md twin exists."""
    if not data_dir.is_dir():
        raise FileNotFoundError(f"Data folder not found: {data_dir.resolve()}")

    docs: list[Any] = []

    # Markdown files
    for md_file in sorted(data_dir.glob("**/*.md")):
        text = md_file.read_text(encoding="utf-8")
        docs.append(Document(page_content=text, metadata={"source": md_file.name}))

    # PDF fallback (only if corresponding .md does not exist)
    for pdf_file in sorted(data_dir.glob("**/*.pdf")):
        if pdf_file.with_suffix(".md").exists():
            continue
        loaded_pages = False
        if PyPDFLoader is not None:
            try:
                pages = PyPDFLoader(str(pdf_file)).load()
                for p in pages:
                    p.metadata["source"] = pdf_file.name
                docs.extend(pages)
                loaded_pages = True
            except Exception as e:
                print(f"Notice: PyPDFLoader error on {pdf_file.name} ({e}), trying fallback reader...")

        if not loaded_pages and pypdf is not None:
            try:
                reader = pypdf.PdfReader(str(pdf_file))
                for idx, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    if text.strip():
                        docs.append(Document(page_content=text, metadata={"source": pdf_file.name, "page": idx}))
                loaded_pages = True
            except Exception as e:
                print(f"Warning: Could not load PDF {pdf_file.name} with pypdf: {e}")

        if not loaded_pages:
            print(f"Warning: Could not load PDF {pdf_file.name}: no working PDF parser available.")

    if not docs:
        raise FileNotFoundError(f"No .md or .pdf files found in {data_dir.resolve()}")

    return docs
