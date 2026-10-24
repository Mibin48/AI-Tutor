import re
from pydantic import BaseModel, Field
from backend.agent.schemas import ToolResult

NAME = "plot_function"
DESCRIPTION = "Plots a mathematical function on the whiteboard coordinate canvas."

ALLOWED_IDENTIFIERS = {"x", "sin", "cos", "tan", "sqrt", "log", "abs", "pi", "e"}
ALLOWED_CHARS_RE = re.compile(r"^[0-9x\s\+\-\*\/\^\(\)\.,]+$")
WORD_RE = re.compile(r"[a-zA-Z_]+")


class Args(BaseModel):
    expression: str = Field(description="Math expression in x (e.g., 'x**2 - 4' or 'sin(x)')")
    x_min: float = Field(-10.0, description="Minimum x range for the plot")
    x_max: float = Field(10.0, description="Maximum x range for the plot")


async def run(args: Args, ctx: dict) -> ToolResult:
    expr = args.expression.strip()
    if not expr:
        return ToolResult(success=False, error="Expression cannot be empty")

    words = WORD_RE.findall(expr)
    for w in words:
        if w.lower() not in ALLOWED_IDENTIFIERS:
            return ToolResult(
                success=False,
                error=f"Disallowed identifier '{w}' in expression. Allowed: {sorted(ALLOWED_IDENTIFIERS)}",
            )

    # Validate that remainder characters are valid math symbols
    stripped_expr = WORD_RE.sub("", expr)
    if not ALLOWED_CHARS_RE.match(stripped_expr):
        return ToolResult(success=False, error=f"Invalid characters in math expression: {expr}")

    x_min, x_max = float(args.x_min), float(args.x_max)
    if x_min >= x_max:
        x_min, x_max = -10.0, 10.0

    return ToolResult(
        success=True,
        payload={
            "tool": NAME,
            "expression": expr,
            "x_min": x_min,
            "x_max": x_max,
        },
    )
