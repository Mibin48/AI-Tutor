from pydantic import BaseModel, Field
from backend.agent.schemas import ToolResult

NAME = "ask_check_question"
DESCRIPTION = "Displays a check question for the student in a 'Your turn' box on the whiteboard."


class Args(BaseModel):
    question: str = Field(description="A concise question to verify student comprehension")


async def run(args: Args, ctx: dict) -> ToolResult:
    q = args.question.strip()
    if not q:
        return ToolResult(success=False, error="Check question cannot be empty")
    return ToolResult(
        success=True,
        payload={"tool": NAME, "question": q},
    )
