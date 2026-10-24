from pydantic import BaseModel, Field
from backend.agent.schemas import ToolResult
from backend.rag.retriever import retrieve

NAME = "search_textbook"
DESCRIPTION = "Runs RAG on the textbook to retrieve context chunks for the question."


class Args(BaseModel):
    query: str = Field(description="Search question or doubt from the student")


async def run(args: Args, ctx: dict) -> ToolResult:
    try:
        history = ctx.get("history", [])
        chunks = retrieve(args.query, history)
        chunks_text = [getattr(c, "page_content", str(c)) for c in chunks]
        context = "\n\n---\n\n".join(chunks_text)
        return ToolResult(
            success=True,
            payload={"context": context, "chunks": chunks_text},
        )
    except Exception as e:
        return ToolResult(success=False, error=str(e), payload={"context": "", "chunks": []})
