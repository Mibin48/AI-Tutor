from pydantic import BaseModel, Field
from backend.agent.schemas import ToolResult

NAME = "write_text"
DESCRIPTION = "Writes a key formula, equation, or short text label on the whiteboard."


class Args(BaseModel):
    text: str = Field(description="Formula or short text label to display on the board")


async def run(args: Args, ctx: dict) -> ToolResult:
    text = args.text.strip()
    if not text:
        return ToolResult(success=False, error="Text cannot be empty")
    return ToolResult(
        success=True,
        payload={"tool": NAME, "text": text},
    )
