from typing import Optional
from pydantic import BaseModel, Field
from backend.agent.schemas import ToolResult

NAME = "write_equation"
DESCRIPTION = "Writes a beautifully formatted mathematical equation involving fractions, rational numbers, or algebraic steps to the whiteboard with LaTeX typography, fraction breakdown, and interactive visualizer."


class Args(BaseModel):
    latex: str = Field(description="LaTeX equation or formula with fractions, e.g. '\\frac{a}{b} + \\frac{c}{d} = \\frac{ad + bc}{bd}' or '\\frac{p}{q}, q \\neq 0'")
    title: Optional[str] = Field("Equation", description="Title or concept label (e.g. 'Rational Number Formula', 'Addition of Fractions')")
    steps: Optional[list[str]] = Field(None, description="Optional step-by-step solving or simplification steps in LaTeX or text")
    description: Optional[str] = Field(None, description="Optional brief mathematical note or rule explanation")
    interactive_slider: Optional[bool] = Field(False, description="Enable an interactive value slider for students to explore variable values")
    variable: Optional[str] = Field("x", description="Variable name for interactive exploration (e.g. 'x')")
    default_val: Optional[float] = Field(1.0, description="Default initial value for the interactive slider")
    min_val: Optional[float] = Field(-10.0, description="Minimum slider range")
    max_val: Optional[float] = Field(10.0, description="Maximum slider range")
    fraction_visualizer: Optional[bool] = Field(True, description="Whether to show interactive fraction / number line visualizer")


async def run(args: Args, ctx: dict) -> ToolResult:
    latex_str = (args.latex or "").strip()
    if not latex_str:
        return ToolResult(success=False, error="LaTeX equation cannot be empty")

    return ToolResult(
        success=True,
        payload={
            "tool": NAME,
            "latex": latex_str,
            "title": args.title or "Equation",
            "steps": args.steps or [],
            "description": args.description or "",
            "interactive_slider": bool(args.interactive_slider),
            "variable": args.variable or "x",
            "default_val": float(args.default_val) if args.default_val is not None else 1.0,
            "min_val": float(args.min_val) if args.min_val is not None else -10.0,
            "max_val": float(args.max_val) if args.max_val is not None else 10.0,
            "fraction_visualizer": bool(args.fraction_visualizer),
        },
    )
