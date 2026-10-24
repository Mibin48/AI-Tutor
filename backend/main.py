from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend import config
from backend.agent.schemas import AskRequest, AskResponse, Step
from backend.agent.demo_data import get_diversified_demo_plan
from backend.agent.study_schemas import QuizRequest, QuizResponse, FlashcardRequest, FlashcardResponse
from backend.agent.study_generator import generate_quiz, generate_flashcards
from backend.agent.tutor_agent import clear_history, execute_answer_pipeline
from backend.tools.play_motion import get_available_motions

app = FastAPI(title="AI Tutor Prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResetRequest(BaseModel):
    session_id: str = "default"


class ProviderRequest(BaseModel):
    provider: str


@app.post("/api/ask", response_model=AskResponse)
async def ask_endpoint(body: AskRequest):
    return await execute_answer_pipeline(body.question, body.session_id or "default", body.provider)


@app.get("/api/provider")
def get_provider_info():
    return {
        "active_provider": config.get_active_provider(),
        "providers": ["auto", "gemini", "openrouter", "ollama"],
        "has_gemini": bool(config.GEMINI_API_KEY),
        "has_openrouter": bool(config.OPENROUTER_API_KEY),
    }


@app.post("/api/provider")
def set_provider_endpoint(body: ProviderRequest):
    config.set_active_provider(body.provider)
    return {"ok": True, "active_provider": config.get_active_provider()}


@app.get("/api/motions")
def list_motions():
    return {"motions": get_available_motions()}


@app.post("/api/reset")
def reset_endpoint(body: ResetRequest | None = None):
    session_id = body.session_id if body else "default"
    clear_history(session_id)
    return {"ok": True}


@app.post("/api/study/quiz", response_model=QuizResponse)
async def create_quiz_endpoint(body: QuizRequest):
    return await generate_quiz(body)


@app.post("/api/study/flashcards", response_model=FlashcardResponse)
async def create_flashcards_endpoint(body: FlashcardRequest):
    return await generate_flashcards(body)


@app.get("/api/demo", response_model=AskResponse)
async def demo_endpoint():
    return await get_diversified_demo_plan()



# Static assets & frontend mounts
app.mount("/motions", StaticFiles(directory=str(config.MOTIONS_DIR)), name="motions")
app.mount("/audio", StaticFiles(directory=str(config.AUDIO_CACHE_DIR)), name="audio")
app.mount("/", StaticFiles(directory=str(config.FRONTEND_DIR), html=True), name="frontend")
