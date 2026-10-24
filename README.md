# AI Tutor Web App Prototype

An interactive AI Tutor web application built for a hackathon. The tutor answers maths doubts by drawing step-by-step on an interactive whiteboard, displaying synchronized chat bubbles, speaking with a natural Indian-English voice (using `edge-tts`), and performing matching animated avatar motions.

---

## Quick Start (One Command)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys (optional for cloud models):**
   Add your keys to `.env` in the project root:
   ```ini
   openrouter = "sk-or-v1-..."
   gemini = "AQ.Ab8..."
   ```

3. **Run the server:**
   ```bash
   uvicorn backend.main:app --port 8000
   ```

4. **Open in browser:**
   Open [http://localhost:8000](http://localhost:8000) in Google Chrome (for Web Speech API support).

---

## AI Model Providers & Cascade

The system supports **three AI engines** with an automatic priority cascade and real-time manual toggling:

```
Default Order: Ollama (Local) ──[if unavailable]──> Gemini (Google AI) ──[if unavailable]──> OpenRouter (Free Tier)
```

1. **Auto (Default Cascade)**:
   - First tries local **Ollama** (`qwen3:4b`).
   - If Ollama is offline or not installed, automatically cascades to **Gemini** (`gemini-3.5-flash-lite`).
   - If Gemini is congested, cascades to **OpenRouter** (free tier models like `nvidia/nemotron-3.5-lightning:free`).
   - If all remote services fail, falls back to the safe local offline plan so the app never crashes.

2. **Manual Engine Selection**:
   - Use the **Engine** dropdown in the top-right header of the web app to lock your preferred provider:
     - `Auto (Ollama → Gemini → OpenRouter)`
     - `Gemini (Google AI)`
     - `OpenRouter (Free Tier)`
     - `Ollama (Local)`
   - Or change it via API: `POST /api/provider {"provider": "gemini"}`.

---

## Study Tools (Quiz & Flashcards Generator)

The web app includes built-in interactive study tools generated directly with **Gemini** (and **OpenRouter** fallback) without requiring textbook RAG:

- **Interactive Practice Quiz (`POST /api/study/quiz`)**:
  - Generates multiple-choice questions with 4 options (A, B, C, D), hints, and step-by-step mathematical reasoning.
  - Interactive whiteboard widget with instant green/red option feedback, score tracker, and retake option.
  - Accessible via the **[📝 Quiz]** button in the whiteboard top bar.

- **3D Revision Flashcards (`POST /api/study/flashcards`)**:
  - Generates flashcards with concept names/formulas on the front and detailed explanations on the back.
  - Interactive 3D flip card widget with previous/next navigation, shuffle, and mastery tracking.
  - Accessible via the **[🗂️ Flashcards]** button in the whiteboard top bar.

---

## Automated Smoke Test

Run the verification suite:
```bash
python -m backend.smoke_test
```
This tests:
1. Tool registry auto-discovery (8 tools).
2. Physical avatar motion discovery (`/api/motions`).
3. Textbook RAG chunk retrieval.
4. AI Providers & API keys (live validation of Gemini and OpenRouter).
5. Canned demo response (`/api/demo`) with real on-the-fly Edge-TTS audio.
6. Study generator suite: Live validation of Quiz and Flashcards generation (Gemini -> OpenRouter, No RAG).

---

## How to Add a New Tool

The architecture follows a strict tool contract. Adding a new tool requires **only two single-responsibility files**:

### 1. Backend Tool
Create a new file in `backend/tools/your_tool.py`:
```python
from pydantic import BaseModel, Field
from backend.agent.schemas import ToolResult

NAME = "your_tool"
DESCRIPTION = "Description for your new whiteboard tool."

class Args(BaseModel):
    my_param: str = Field(description="Parameter description")

async def run(args: Args, ctx: dict) -> ToolResult:
    return ToolResult(success=True, payload={"tool": NAME, "param": args.my_param})
```
*No registry edits needed!* `backend/tools/__init__.py` will auto-discover and register your tool automatically.

### 2. Frontend Whiteboard Tool
Create `frontend/src/whiteboard/tools/yourTool.js`:
```javascript
export function render(board, payload) {
  const container = document.createElement("div");
  container.textContent = payload.param;
  return board.addBox("Your Tool Label", container, "box-your-tool");
}
```
Then add one line to the registry in `frontend/src/whiteboard/tools/index.js`:
```javascript
import * as yourTool from "./yourTool.js";
// In REGISTRY:
your_tool: yourTool.render,
```

---

## How to Add a Motion Video

1. Place your `.mp4` video file directly into `assets/motions/` (e.g., `assets/motions/Explaining.mp4`).
2. The backend automatically detects it on `/api/motions`.
3. The LLM prompt and avatar player will dynamically incorporate the new motion name without any code modifications.
