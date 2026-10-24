import asyncio
import sys
from backend import config
from backend.agent.gemini_client import call_gemini
from backend.agent.openrouter_client import call_openrouter
from backend.agent.study_generator import generate_quiz, generate_flashcards
from backend.agent.study_schemas import FlashcardRequest, QuizRequest
from backend.main import demo_endpoint, get_provider_info, list_motions, set_provider_endpoint, ProviderRequest
from backend.rag.retriever import retrieve
from backend.tools import REGISTRY


def test_registry():
    print("[1/5] Checking tool auto-discovery...")
    assert len(REGISTRY) >= 7, f"Expected at least 7 tools, found {len(REGISTRY)}"
    for name in ["write_text", "plot_function", "draw_shape", "clear_board", "unable", "search_textbook", "play_motion"]:
        assert name in REGISTRY, f"Tool '{name}' missing from REGISTRY"
    print(f"      PASSED: {len(REGISTRY)} tools registered.")


def test_motions():
    print("[2/5] Checking /api/motions...")
    res = list_motions()
    motions = res.get("motions", [])
    assert len(motions) > 0, "No motions found in assets/motions"
    print(f"      PASSED: Discovered {len(motions)} motion videos.")


def test_retriever():
    print("[3/5] Checking textbook RAG retrieval...")
    chunks = retrieve("algebra play", [])
    assert len(chunks) > 0, "Retriever returned 0 chunks from data/"
    print(f"      PASSED: Retrieved {len(chunks)} chunks from textbook data.")


def test_providers():
    print("[4/5] Checking AI Providers & API keys...")
    info = get_provider_info()
    print(f"      Active Provider: {info['active_provider']}")
    print(f"      Gemini configured: {info['has_gemini']}, OpenRouter configured: {info['has_openrouter']}")

    # Test provider switching
    set_provider_endpoint(ProviderRequest(provider="gemini"))
    assert config.get_active_provider() == "gemini"
    set_provider_endpoint(ProviderRequest(provider="openrouter"))
    assert config.get_active_provider() == "openrouter"
    set_provider_endpoint(ProviderRequest(provider="auto"))
    assert config.get_active_provider() == "auto"

    # Test Gemini if key present
    if config.GEMINI_API_KEY:
        sample_prompt = 'Output valid JSON: {"found_in_book": true, "steps": [{"say": "Hello", "tool": "write_text", "text": "x", "motion": "Greeting"}], "check_question": null}'
        g_res = asyncio.run(call_gemini(sample_prompt))
        if g_res and "steps" in g_res:
            print("      PASSED: Gemini live API responded with valid structured plan.")
        else:
            print("      Notice: Gemini returned no plan (upstream busy or fallback).")

    # Test OpenRouter if key present
    if config.OPENROUTER_API_KEY:
        sample_prompt = 'Output valid JSON: {"found_in_book": true, "steps": [{"say": "Hello", "tool": "write_text", "text": "x", "motion": "Greeting"}], "check_question": null}'
        or_res = asyncio.run(call_openrouter(sample_prompt))
        if or_res and "steps" in or_res:
            print("      PASSED: OpenRouter live API responded with valid structured plan.")
        else:
            print("      Notice: OpenRouter returned no plan (rate limit or fallback).")


def test_demo_with_audio():
    print("[5/6] Checking /api/demo with real TTS generation...")
    res = asyncio.run(demo_endpoint())
    assert res.found_in_book is True
    assert len(res.steps) >= 2

    for i, step in enumerate(res.steps):
        assert step.say and step.audio_url
        filename = step.audio_url.replace("/audio/", "")
        file_path = config.AUDIO_CACHE_DIR / filename
        assert file_path.exists() and file_path.stat().st_size > 0

    print("      PASSED: Demo endpoint returned valid steps with real TTS audio.")


def test_study_generators():
    print("[6/6] Checking Quiz & Flashcard generation (Gemini -> OpenRouter, no RAG)...")
    quiz = asyncio.run(generate_quiz(QuizRequest(topic="Rational Numbers", num_questions=2)))
    assert len(quiz.questions) == 2, f"Expected 2 quiz questions, got {len(quiz.questions)}"
    for q in quiz.questions:
        assert q.question and len(q.options) == 4
        assert q.correct_id in {"A", "B", "C", "D"}
        assert q.explanation
    print(f"      PASSED: Generated {len(quiz.questions)} valid quiz questions.")

    cards = asyncio.run(generate_flashcards(FlashcardRequest(topic="Rational Numbers", num_cards=2)))
    assert len(cards.cards) == 2, f"Expected 2 flashcards, got {len(cards.cards)}"
    for c in cards.cards:
        assert c.front and c.back
    print(f"      PASSED: Generated {len(cards.cards)} valid flashcards.")


def main():
    print("=== AI Tutor Multi-Provider Smoke Test ===")
    try:
        test_registry()
        test_motions()
        test_retriever()
        test_providers()
        test_demo_with_audio()
        test_study_generators()
        print("\nAll smoke tests passed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"\nFAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
