import asyncio
from typing import Any
from backend import config
from backend.agent.gemini_client import call_gemini
from backend.agent.openrouter_client import call_openrouter
from backend.agent.prompts import SYSTEM_PROMPT
from backend.agent.schemas import AskResponse, Step, StepPlan, TutorPlan
from backend.tools import REGISTRY, get_tool
from backend.tools.play_motion import get_available_motions
from backend.voice.tts import get_tts_engine

_SESSIONS: dict[str, list[tuple[str, str]]] = {}


def clear_history(session_id: str = "default") -> None:
    if session_id in _SESSIONS:
        _SESSIONS[session_id].clear()


def get_history(session_id: str = "default") -> list[tuple[str, str]]:
    return _SESSIONS.setdefault(session_id, [])


def _build_mock_plan(question: str, context: str) -> TutorPlan:
    q = question.lower()
    motions = get_available_motions() or ["Talking", "Pointing", "Thinking"]
    m_talk, m_point, m_praise = motions[0], motions[min(1, len(motions)-1)], motions[min(2, len(motions)-1)]

    if "trick" in q or "number" in q or "algebra" in q:
        return TutorPlan(
            found_in_book=True,
            steps=[
                StepPlan(say="In algebra play, we can use x to represent any mystery number.",
                         tool="write_text", text="x -> 2x -> 2x + 4 -> x + 2 -> 2", motion=m_talk),
                StepPlan(say="When we subtract our original number x, the result is always two.",
                         tool="plot_function", expression="x + 2 - x", x_min=-5, x_max=5, motion=m_point),
                StepPlan(say="Algebra explains why the trick works for every single number.",
                         tool="draw_shape", shape="circle", motion=m_praise),
            ],
            check_question="Can you change the steps so the answer is always five?",
        )
    return TutorPlan(
        found_in_book=True if context else False,
        steps=[StepPlan(say="Here is what our textbook chapter explains about this concept.",
                        tool="write_text", text=context.split("\n")[0][:60] or "Key Concept", motion=m_talk)],
        check_question="Would you like to explore an example together?",
    )


async def _try_ollama(prompt: str, history: list, question: str) -> TutorPlan | None:
    try:
        from langchain_ollama import ChatOllama
        messages = [("system", prompt)]
        for u, a in history[-config.MAX_HISTORY_TURNS:]:
            messages.append(("human", u))
            messages.append(("ai", a))
        messages.append(("human", question))
        llm = ChatOllama(model=config.LLM_MODEL, temperature=0.2)
        return await llm.with_structured_output(TutorPlan, method="json_schema").ainvoke(messages)
    except Exception:
        return None


async def _run_llm(context: str, question: str, history: list[tuple[str, str]], provider: str | None = None) -> TutorPlan:
    mode = provider or config.get_active_provider()
    allowed_tools = [k for k in REGISTRY.keys() if k != "search_textbook"]
    allowed_motions = get_available_motions()
    hist_text = "\n".join(f"Student: {u}\nTutor: {a}" for u, a in history[-config.MAX_HISTORY_TURNS:])
    prompt = (
        f"{SYSTEM_PROMPT.format(allowed_tools=', '.join(allowed_tools), allowed_motions=', '.join(allowed_motions), context=context)}\n"
        f"Previous turns:\n{hist_text}\nStudent question: {question}\nOutput valid JSON for TutorPlan."
    )

    # 1. Ollama (if requested or in auto cascade)
    if mode in {"ollama", "auto"}:
        res = await _try_ollama(prompt, history, question)
        if res:
            return res
        if mode == "ollama":
            return _build_mock_plan(question, context)

    # 2. Gemini (if requested or in auto cascade)
    if mode in {"gemini", "auto"}:
        res_dict = await call_gemini(prompt)
        if res_dict:
            try:
                return TutorPlan.model_validate(res_dict)
            except Exception as e:
                print("Gemini validation warning:", e)
        if mode == "gemini":
            return _build_mock_plan(question, context)

    # 3. OpenRouter (if requested or in auto cascade)
    if mode in {"openrouter", "auto"}:
        res_dict = await call_openrouter(prompt)
        if res_dict:
            try:
                return TutorPlan.model_validate(res_dict)
            except Exception as e:
                print("OpenRouter validation warning:", e)

    # 4. Fallback plan
    return _build_mock_plan(question, context)


async def _validate_step(step: StepPlan) -> Step | None:
    tool_entry = get_tool(step.tool)
    if not tool_entry:
        return None
    raw_args: dict[str, Any] = {}
    if step.tool == "write_text":
        txt = (step.text or "").strip()
        if not txt or txt.lower() in {"math concept", "concept", "null", "none"}:
            txt = (step.say or "").strip()
        raw_args["text"] = txt or "Key Concept"
    elif step.tool == "plot_function":
        raw_args["expression"] = step.expression or "x"
        raw_args["x_min"] = step.x_min if step.x_min is not None else -10.0
        raw_args["x_max"] = step.x_max if step.x_max is not None else 10.0
    elif step.tool == "draw_shape":
        raw_args["shape"] = step.shape or "rectangle"
    elif step.tool == "unable":
        raw_args["message"] = step.unable_reason or "Not covered in chapter"

    try:
        res = await tool_entry.run(tool_entry.args_schema(**raw_args), {})
        if not res.success:
            return None
        motion_tool = get_tool("play_motion")
        m_res = await motion_tool.run(motion_tool.args_schema(motion=step.motion), {})
        return Step(say=step.say, motion=m_res.payload.get("motion", step.motion), board=res.payload)
    except Exception:
        return None


async def execute_answer_pipeline(question: str, session_id: str = "default", provider: str | None = None) -> AskResponse:
    history = get_history(session_id)
    search_tool = get_tool("search_textbook")
    search_res = await search_tool.run(search_tool.args_schema(query=question), {"history": history})
    context = search_res.payload.get("context", "")

    plan = await _run_llm(context, question, history, provider)
    valid_steps: list[Step] = []
    for s in plan.steps:
        v = await _validate_step(s)
        if v:
            valid_steps.append(v)

    if not valid_steps or valid_steps[0].board.get("tool") not in {"write_text", "unable"}:
        unable_tool = get_tool("unable")
        u_res = await unable_tool.run(unable_tool.args_schema(message="Unable to verify explanation"), {})
        valid_steps = [Step(say="I am unable to answer this from the textbook.", motion="Neutral", board=u_res.payload)]

    tts = get_tts_engine()
    audio_urls = await asyncio.gather(*[tts.synthesize(s.say) for s in valid_steps])
    for s, url in zip(valid_steps, audio_urls):
        s.audio_url = url

    full_speech = " ".join(s.say for s in valid_steps)
    history.append((question, full_speech))
    if len(history) > config.MAX_HISTORY_TURNS:
        del history[:-config.MAX_HISTORY_TURNS]

    return AskResponse(found_in_book=plan.found_in_book, steps=valid_steps, check_question=plan.check_question)
