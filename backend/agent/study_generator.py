import json
from backend import config
from backend.agent.gemini_client import call_gemini
from backend.agent.openrouter_client import call_openrouter
from backend.agent.study_schemas import (
    FlashcardRequest,
    FlashcardResponse,
    QuizRequest,
    QuizResponse,
)
from backend.agent.study_templates import (
    build_offline_quiz,
    build_offline_flashcards,
)


async def generate_quiz(req: QuizRequest) -> QuizResponse:
    """Generate an educational multiple-choice quiz without RAG.

    Cascade: Gemini -> OpenRouter -> Offline fallback.
    """
    mode = req.provider or config.get_active_provider()

    prompt = (
        f"You are a master mathematics tutor creating an interactive quiz for school students.\n"
        f"Generate a {req.difficulty}-level quiz on the topic: '{req.topic}'.\n"
        f"Generate exactly {req.num_questions} multiple choice questions.\n\n"
        f"CRITICAL RULES:\n"
        f"1. Rely purely on mathematical accuracy (NO RAG or external documents needed).\n"
        f"2. Each question MUST contain exactly 4 options labeled 'A', 'B', 'C', 'D'.\n"
        f"3. 'correct_id' must be one of: 'A', 'B', 'C', 'D'.\n"
        f"4. Provide a clear, educational step-by-step 'explanation' for the solution.\n"
        f"5. Output valid JSON matching this schema:\n"
        f"{{\n"
        f'  "topic": "{req.topic}",\n'
        f'  "difficulty": "{req.difficulty}",\n'
        f'  "questions": [\n'
        f"    {{\n"
        f'      "id": 1,\n'
        f'      "question": "Question text",\n'
        f'      "options": [\n'
        f'        {{"id": "A", "text": "Option A"}},\n'
        f'        {{"id": "B", "text": "Option B"}},\n'
        f'        {{"id": "C", "text": "Option C"}},\n'
        f'        {{"id": "D", "text": "Option D"}}\n'
        f"      ],\n"
        f'      "correct_id": "A",\n'
        f'      "explanation": "Why A is correct step-by-step",\n'
        f'      "hint": "Helpful hint"\n'
        f"    }}\n"
        f"  ]\n"
        f"}}"
    )

    # 1. Try Gemini (default cascade or explicit)
    if mode in {"auto", "gemini"}:
        try:
            res = await call_gemini(prompt, required_key="questions")
            if res and "questions" in res and len(res["questions"]) > 0:
                res["topic"] = req.topic
                res["difficulty"] = req.difficulty
                return QuizResponse.model_validate(res)
        except Exception as e:
            print(f"Notice: Gemini quiz generation failed: {e}")

    # 2. Try OpenRouter fallback
    if mode in {"auto", "openrouter"} or (mode == "gemini" and config.OPENROUTER_API_KEY):
        try:
            res = await call_openrouter(prompt, required_key="questions")
            if res and "questions" in res and len(res["questions"]) > 0:
                res["topic"] = req.topic
                res["difficulty"] = req.difficulty
                return QuizResponse.model_validate(res)
        except Exception as e:
            print(f"Notice: OpenRouter quiz generation failed: {e}")

    # 3. Safe Offline Fallback
    return build_offline_quiz(req.topic, req.difficulty, req.num_questions)


async def generate_flashcards(req: FlashcardRequest) -> FlashcardResponse:
    """Generate educational revision flashcards without RAG.

    Cascade: Gemini -> OpenRouter -> Offline fallback.
    """
    mode = req.provider or config.get_active_provider()

    prompt = (
        f"You are a master mathematics tutor creating revision flashcards for school students.\n"
        f"Generate {req.num_cards} flashcards on the topic: '{req.topic}' at {req.difficulty} difficulty.\n\n"
        f"CRITICAL RULES:\n"
        f"1. Rely purely on mathematical accuracy (NO RAG or external documents needed).\n"
        f"2. Front: concise concept question, formula name, or key term.\n"
        f"3. Back: clear definition, formula, example, or step-by-step breakdown.\n"
        f"4. Category: one of 'Concept', 'Formula', 'Rule', or 'Example'.\n"
        f"5. Output valid JSON matching this schema:\n"
        f"{{\n"
        f'  "topic": "{req.topic}",\n'
        f'  "cards": [\n'
        f"    {{\n"
        f'      "id": 1,\n'
        f'      "front": "Card front text",\n'
        f'      "back": "Card back text",\n'
        f'      "category": "Concept"\n'
        f"    }}\n"
        f"  ]\n"
        f"}}"
    )

    # 1. Try Gemini
    if mode in {"auto", "gemini"}:
        try:
            res = await call_gemini(prompt, required_key="cards")
            if res and "cards" in res and len(res["cards"]) > 0:
                res["topic"] = req.topic
                return FlashcardResponse.model_validate(res)
        except Exception as e:
            print(f"Notice: Gemini flashcard generation failed: {e}")

    # 2. Try OpenRouter fallback
    if mode in {"auto", "openrouter"} or (mode == "gemini" and config.OPENROUTER_API_KEY):
        try:
            res = await call_openrouter(prompt, required_key="cards")
            if res and "cards" in res and len(res["cards"]) > 0:
                res["topic"] = req.topic
                return FlashcardResponse.model_validate(res)
        except Exception as e:
            print(f"Notice: OpenRouter flashcard generation failed: {e}")

    # 3. Safe Offline Fallback
    return build_offline_flashcards(req.topic, req.difficulty, req.num_cards)
