import asyncio
from backend.agent.schemas import AskResponse, Step
from backend.tools.play_motion import get_available_motions
from backend.voice.tts import get_tts_engine


async def get_diversified_demo_plan() -> AskResponse:
    """Generates a complete, diversified masterclass demonstration on Rational Numbers

    showcasing all AI tutor tools: NCERT textbook RAG retrieval, number line visualizer,
    algebraic equation breakdown with interactive variable slider, coordinate function graphing,
    3D flip revision flashcards, and an interactive quiz.
    """
    tts = get_tts_engine()

    s1_text = (
        "Welcome to our math masterclass on Rational Numbers! I retrieve lesson material directly from your NCERT Class 8 textbook using RAG. A rational number is any number expressible as p divided by q, where p and q are integers and q cannot equal zero."
    )
    s2_text = (
        "Every rational number occupies a distinct spot on the continuous number line. Notice how negative fractions lie to the left of zero, while positive numbers like three-fourths and four-thirds extend to the right."
    )
    s3_text = (
        "Rational numbers obey core arithmetic rules. They are closed under addition, subtraction, and multiplication. Zero acts as the additive identity, and non-zero numbers have a reciprocal. Try adjusting the variable p on the whiteboard slider!"
    )
    s4_text = (
        "Let's graph the fundamental rational function y equals one over x. Observe the two symmetrical hyperbolic branches. Near zero, the curve splits towards positive and negative infinity, visually proving why the denominator q can never equal zero."
    )
    s5_text = (
        "To help you excel in exams, I generate interactive 3D flashcards. Tap or click any card on the whiteboard to flip between definitions, properties, and reciprocal rules."
    )
    s6_text = (
        "Now test your mastery with an interactive quiz! Select your choice below to receive immediate step-by-step scoring, hints, and explanations."
    )

    audio_urls = await asyncio.gather(
        tts.synthesize(s1_text),
        tts.synthesize(s2_text),
        tts.synthesize(s3_text),
        tts.synthesize(s4_text),
        tts.synthesize(s5_text),
        tts.synthesize(s6_text),
    )

    motions = get_available_motions()
    m_greet = "Greeting" if "Greeting" in motions else "Talking"
    m_point = "Pointing" if "Pointing" in motions else "Talking"
    m_talk = "Talking" if "Talking" in motions else "Neutral"
    m_praise = "Praising" if "Praising" in motions else "Talking"
    m_celeb = "Celebrating" if "Celebrating" in motions else "Praising"

    steps = [
        Step(
            say=s1_text,
            audio_url=audio_urls[0],
            motion=m_greet,
            board={
                "tool": "write_text",
                "title": "NCERT Textbook Retrieval",
                "text": "📖 NCERT Class 8 Mathematics • Chapter 1: Rational Numbers\nSection 1.1: Standard Definition\nA number that can be expressed in the form p/q, where p and q are integers and q ≠ 0, is called a rational number.\nExamples: 2/3, -5/7, 0 (= 0/1), and 4 (= 4/1).",
            },
        ),
        Step(
            say=s2_text,
            audio_url=audio_urls[1],
            motion=m_point,
            board={
                "tool": "draw_shape",
                "title": "Number Line Representation",
                "shape": "number_line",
                "caption": "NCERT Chapter 1: Representation of Rational Numbers on the Number Line",
            },
        ),
        Step(
            say=s3_text,
            audio_url=audio_urls[2],
            motion=m_talk,
            board={
                "tool": "write_equation",
                "title": "Rational Arithmetic & Properties",
                "latex": r"\frac{a}{b} + \frac{c}{d} = \frac{ad + bc}{bd} \quad (b \neq 0, d \neq 0)",
                "steps": [
                    "1. Closure: For any two rational numbers, their sum, difference, and product are always rational.",
                    "2. Additive Identity: 0 is the additive identity (a/b + 0 = a/b).",
                    "3. Additive Inverse: The negative of a/b is -a/b, such that (a/b) + (-a/b) = 0.",
                    "4. Reciprocal: For non-zero a/b, its multiplicative inverse is b/a, such that (a/b) × (b/a) = 1.",
                ],
                "description": "Crucial rule: Zero has NO reciprocal, because division by zero is undefined in mathematics!",
                "interactive_slider": True,
                "variable": "p",
                "default_val": 3.0,
                "min_val": -5.0,
                "max_val": 5.0,
            },
        ),
        Step(
            say=s4_text,
            audio_url=audio_urls[3],
            motion=m_talk,
            board={
                "tool": "plot_function",
                "expression": "1 / x",
                "x_min": -4.0,
                "x_max": 4.0,
            },
        ),
        Step(
            say=s5_text,
            audio_url=audio_urls[4],
            motion=m_praise,
            board={
                "tool": "flashcards",
                "topic": "Rational Numbers Mastery",
                "cards": [
                    {
                        "front": "Standard Rational Definition",
                        "back": "A number expressible as p/q, where p, q ∈ ℤ and q ≠ 0.\nExamples: 3/5, -7/2, 0, 8.",
                        "category": "Definition",
                    },
                    {
                        "front": "Closure Property",
                        "back": "Closed under Addition, Subtraction, and Multiplication.\nNOT closed under division because division by zero is undefined.",
                        "category": "Property",
                    },
                    {
                        "front": "Additive Identity & Inverse",
                        "back": "Additive Identity is 0: a + 0 = a.\nAdditive Inverse of a/b is -a/b, where (a/b) + (-a/b) = 0.",
                        "category": "Formula",
                    },
                    {
                        "front": "Multiplicative Inverse (Reciprocal)",
                        "back": "For any non-zero rational a/b, its reciprocal is b/a.\nImportant: 0 has NO reciprocal!",
                        "category": "Rule",
                    },
                    {
                        "front": "Density Property",
                        "back": "Between any two rational numbers, there are infinitely many rational numbers!\nMidpoint formula: (a + b) / 2.",
                        "category": "Concept",
                    },
                ],
            },
        ),
        Step(
            say=s6_text,
            audio_url=audio_urls[5],
            motion=m_celeb,
            board={
                "tool": "quiz",
                "topic": "Rational Numbers Quick Check",
                "difficulty": "medium",
                "questions": [
                    {
                        "id": "q1",
                        "question": "Which of the following numbers is NOT a rational number?",
                        "options": [
                            {"id": "A", "text": "3 / 4"},
                            {"id": "B", "text": "0"},
                            {"id": "C", "text": "-5"},
                            {"id": "D", "text": "7 / 0"},
                        ],
                        "correct_id": "D",
                        "explanation": "Division by zero is undefined! A rational number requires denominator q ≠ 0 in p/q. Zero itself is rational (0/1), but 7/0 is undefined.",
                        "hint": "Remember the condition for denominator q in p/q.",
                    },
                    {
                        "id": "q2",
                        "question": "What is the additive inverse of -4/9?",
                        "options": [
                            {"id": "A", "text": "4 / 9"},
                            {"id": "B", "text": "-9 / 4"},
                            {"id": "C", "text": "9 / 4"},
                            {"id": "D", "text": "0"},
                        ],
                        "correct_id": "A",
                        "explanation": "The additive inverse of a/b is -a/b, so -(-4/9) = +4/9, since -4/9 + 4/9 = 0.",
                        "hint": "Find the number that sums with -4/9 to produce zero.",
                    },
                    {
                        "id": "q3",
                        "question": "What is the reciprocal (multiplicative inverse) of -5/8?",
                        "options": [
                            {"id": "A", "text": "5 / 8"},
                            {"id": "B", "text": "-8 / 5"},
                            {"id": "C", "text": "8 / 5"},
                            {"id": "D", "text": "-1"},
                        ],
                        "correct_id": "B",
                        "explanation": "The reciprocal of p/q is q/p. Inverting -5/8 gives -8/5, because (-5/8) × (-8/5) = 1.",
                        "hint": "Swap numerator and denominator while keeping the negative sign.",
                    },
                ],
            },
        ),
    ]

    return AskResponse(
        found_in_book=True,
        steps=steps,
        check_question="Can you explain why zero is a rational number, but the fraction 5 divided by zero is undefined?",
    )
