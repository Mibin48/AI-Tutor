from pathlib import Path
from pydantic import BaseModel, Field
from backend import config
from backend.agent.schemas import ToolResult

NAME = "play_motion"
DESCRIPTION = "Validates the motion name against real video files located in assets/motions."


def get_available_motions() -> list[str]:
    """Discover all motion names from existing mp4 files in assets/motions."""
    if not config.MOTIONS_DIR.exists():
        return []
    motions = []
    for file in sorted(config.MOTIONS_DIR.glob("*.mp4")):
        motions.append(file.stem)
    return motions


class Args(BaseModel):
    motion: str = Field(description="Motion name to trigger for the avatar")


async def run(args: Args, ctx: dict) -> ToolResult:
    available = get_available_motions()
    if not available:
        return ToolResult(success=True, payload={"motion": args.motion})

    # Case-insensitive resolution
    target = args.motion.strip().lower()
    for m in available:
        if m.lower() == target:
            return ToolResult(success=True, payload={"motion": m})

    # Fallback to first available or 'Neutral'/'Greeting' if motion not found
    fallback = next((m for m in available if m.lower() in {"neutral", "greeting", "talking"}), available[0])
    return ToolResult(
        success=True,
        payload={"motion": fallback, "warning": f"Motion '{args.motion}' resolved to fallback '{fallback}'"},
    )
