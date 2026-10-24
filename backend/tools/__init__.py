import importlib
from pathlib import Path
from typing import Any, Callable, NamedTuple, Type
from pydantic import BaseModel


class ToolEntry(NamedTuple):
    name: str
    description: str
    args_schema: Type[BaseModel]
    run: Callable[[Any, dict], Any]


REGISTRY: dict[str, ToolEntry] = {}


def get_tool(name: str) -> ToolEntry | None:
    return REGISTRY.get(name)


def get_all_tools() -> list[ToolEntry]:
    return list(REGISTRY.values())


def _discover_tools():
    tools_dir = Path(__file__).resolve().parent
    for py_file in sorted(tools_dir.glob("*.py")):
        if py_file.name.startswith("__"):
            continue
        module_name = f"backend.tools.{py_file.stem}"
        try:
            mod = importlib.import_module(module_name)
            name = getattr(mod, "NAME", None)
            desc = getattr(mod, "DESCRIPTION", None)
            args_cls = getattr(mod, "Args", None)
            run_fn = getattr(mod, "run", None)

            if name and desc and args_cls and run_fn:
                REGISTRY[name] = ToolEntry(
                    name=name,
                    description=desc,
                    args_schema=args_cls,
                    run=run_fn,
                )
        except Exception as e:
            print(f"Error loading tool module {module_name}: {e}")


_discover_tools()


__all__ = ["REGISTRY", "ToolEntry", "get_tool", "get_all_tools"]
