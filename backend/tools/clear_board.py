from pydantic import BaseModel
from backend.agent.schemas import ToolResult

NAME = "clear_board"
DESCRIPTION = "Clears all blocks currently visible on the whiteboard."


class Args(BaseModel):
    pass


async def run(args: Args, ctx: dict) -> ToolResult:
    return ToolResult(
        success=True,
        payload={"tool": NAME},
    )
