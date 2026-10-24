from typing import Literal
from pydantic import BaseModel, Field
from backend.agent.schemas import ToolResult

NAME = "draw_shape"
DESCRIPTION = "Draws a 2D geometric shape (line, circle, triangle, rectangle) on the whiteboard."


class Args(BaseModel):
    shape: Literal["line", "circle", "triangle", "rectangle"] = Field(
        description="The geometric shape to draw on the whiteboard"
    )


async def run(args: Args, ctx: dict) -> ToolResult:
    shape = args.shape.lower().strip()
    if shape not in {"line", "circle", "triangle", "rectangle"}:
        return ToolResult(success=False, error=f"Unknown shape: {args.shape}")

    return ToolResult(
        success=True,
        payload={"tool": NAME, "shape": shape},
    )
