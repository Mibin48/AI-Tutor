import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INDEX_DIR = BASE_DIR / "tutor_index"
ASSETS_DIR = BASE_DIR / "assets"
MOTIONS_DIR = ASSETS_DIR / "motions"
AUDIO_CACHE_DIR = Path("/tmp/audio") if os.environ.get("VERCEL") else ASSETS_DIR / "audio"
FRONTEND_DIR = BASE_DIR / "frontend"

# Ensure runtime directories exist safely (using /tmp on serverless environments like Vercel)
try:
    AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    MOTIONS_DIR.mkdir(parents=True, exist_ok=True)
    FRONTEND_DIR.mkdir(parents=True, exist_ok=True)
except OSError:
    pass

# Parse .env if present
ENV_VARS: dict[str, str] = {}
env_file = BASE_DIR / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        ENV_VARS[k.strip().lower()] = v.strip().strip("'\"")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or ENV_VARS.get("openrouter") or ENV_VARS.get("openrouter_api_key", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ENV_VARS.get("gemini") or ENV_VARS.get("gemini_api_key", "")

# AI Provider state: "auto", "gemini", "openrouter", "ollama"
DEFAULT_PROVIDER = os.getenv("AI_PROVIDER") or ENV_VARS.get("ai_provider", "auto")
_active_provider = DEFAULT_PROVIDER


def get_active_provider() -> str:
    return _active_provider


def set_active_provider(provider: str) -> None:
    global _active_provider
    if provider in {"auto", "gemini", "openrouter", "ollama"}:
        _active_provider = provider


# Model Lists
OPENROUTER_MODELS = [
    "nvidia/nemotron-3.5-lightning:free",
    "dots-studio/dots-3-note-preview:free",
    "xingchen-agi/xing4.0-29b-a4b:free",
    "google/gemma-4-31b-it:free",
]

GEMINI_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-3-flash-preview",
]

# AI Models (Ollama)
EMBED_MODEL = "bge-m3"
LLM_MODEL = "qwen3:4b"

# Voice Configuration
VOICE = "en-IN-NeerjaNeural"

# RAG & Context Parameters
CHUNK_SIZE = 900
CHUNK_OVERLAP = 120
TOP_K = 4
MAX_HISTORY_TURNS = 3
