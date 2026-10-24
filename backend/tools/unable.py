from typing import Optional
from pydantic import BaseModel, Field
from backend.agent.schemas import ToolResult

NAME = "unable"
DESCRIPTION = "Displays a notice on the whiteboard when a question is outside the textbook or an error occurs."


class Args(BaseModel):
    message: Optional[str] = Field(
        default="This concept is not covered in our current textbook chapter.",
        description="Reason or notice message to display on the board",
    )


async def run(args: Args, ctx: dict) -> ToolResult:
    msg = (args.message or "").strip() or "This concept is not covered in our current textbook chapter."
    return ToolResult(
        success=True,
        payload={"tool": NAME, "message": msg},
    )
