from backend.agent.study_schemas import (
    Flashcard,
    FlashcardResponse,
    QuizOption,
    QuizQuestion,
    QuizResponse,
)


def build_offline_quiz(topic: str, difficulty: str, count: int) -> QuizResponse:
    """Offline rule-based fallback when neither Gemini nor OpenRouter is reachable."""
    q_lower = topic.lower()

    if "rational" in q_lower or "number" in q_lower:
        base_questions = [
            QuizQuestion(
                id=1,
                question="Which of the following numbers is a rational number?",
                options=[
                    QuizOption(id="A", text="√2"),
                    QuizOption(id="B", text="π"),
                    QuizOption(id="C", text="-3/5"),
                    QuizOption(id="D", text="√7"),
                ],
                correct_id="C",
                explanation="A rational number can be written as p/q where p and q are integers and q ≠ 0. Here, -3/5 is the ratio of integers -3 and 5.",
                hint="Look for a number written as a fraction of integers.",
            ),
            QuizQuestion(
                id=2,
                question="What is the additive inverse of -7/19?",
                options=[
                    QuizOption(id="A", text="7/19"),
                    QuizOption(id="B", text="-19/7"),
                    QuizOption(id="C", text="19/7"),
                    QuizOption(id="D", text="0"),
                ],
                correct_id="A",
                explanation="The additive inverse of a number a/b is -(a/b) because their sum is zero: (-7/19) + (7/19) = 0.",
                hint="Additive inverse means the number that adds up to 0.",
            ),
            QuizQuestion(
                id=3,
                question="Which property states that a/b * (c/d + e/f) = (a/b * c/d) + (a/b * e/f)?",
                options=[
                    QuizOption(id="A", text="Commutative property"),
                    QuizOption(id="B", text="Associative property"),
                    QuizOption(id="C", text="Distributive property of multiplication over addition"),
                    QuizOption(id="D", text="Closure property"),
                ],
                correct_id="C",
                explanation="The distributive property allows multiplication to be distributed across each term inside the parenthesis.",
                hint="Notice how the factor outside is distributed to both inside terms.",
            ),
            QuizQuestion(
                id=4,
                question="What is the reciprocal (multiplicative inverse) of -13/25?",
                options=[
                    QuizOption(id="A", text="13/25"),
                    QuizOption(id="B", text="-25/13"),
                    QuizOption(id="C", text="25/13"),
                    QuizOption(id="D", text="1"),
                ],
                correct_id="B",
                explanation="The reciprocal of a/b is b/a such that their product is 1. The reciprocal of -13/25 is -25/13.",
                hint="Swap numerator and denominator while keeping the sign.",
            ),
        ]
    elif "linear" in q_lower or "equation" in q_lower or "algebra" in q_lower:
        base_questions = [
            QuizQuestion(
                id=1,
                question="Solve for x: 3x - 7 = 14",
                options=[
                    QuizOption(id="A", text="x = 5"),
                    QuizOption(id="B", text="x = 7"),
                    QuizOption(id="C", text="x = 21"),
                    QuizOption(id="D", text="x = 3"),
                ],
                correct_id="B",
                explanation="Add 7 to both sides: 3x = 21. Divide both sides by 3: x = 7.",
                hint="Isolate 3x first by adding 7 to 14.",
            ),
            QuizQuestion(
                id=2,
                question="What is the degree of a linear equation in one variable?",
                options=[
                    QuizOption(id="A", text="0"),
                    QuizOption(id="B", text="1"),
                    QuizOption(id="C", text="2"),
                    QuizOption(id="D", text="Variable"),
                ],
                correct_id="B",
                explanation="A linear equation has its highest variable power (exponent) equal to 1.",
                hint="Linear implies a straight line whose variable exponent is unity.",
            ),
            QuizQuestion(
                id=3,
                question="If 2(x + 3) = 16, what is the value of x?",
                options=[
                    QuizOption(id="A", text="x = 4"),
                    QuizOption(id="B", text="x = 5"),
                    QuizOption(id="C", text="x = 8"),
                    QuizOption(id="D", text="x = 10"),
                ],
                correct_id="B",
                explanation="Divide both sides by 2: x + 3 = 8. Subtract 3: x = 5.",
                hint="Divide by 2 first or expand 2x + 6 = 16.",
            ),
        ]
    else:
        base_questions = [
            QuizQuestion(
                id=1,
                question=f"In the study of {topic}, which of the following statements is mathematically true?",
                options=[
                    QuizOption(id="A", text="Properties are preserved under valid equality operations"),
                    QuizOption(id="B", text="Division by zero is always defined as 0"),
                    QuizOption(id="C", text="Signs do not matter when multiplying negative values"),
                    QuizOption(id="D", text="Equations only have integer solutions"),
                ],
                correct_id="A",
                explanation="Performing the same operation on both sides of an equality preserves mathematical truth.",
                hint="Think about fundamental algebraic axioms.",
            ),
            QuizQuestion(
                id=2,
                question=f"What is a key foundational concept when mastering {topic}?",
                options=[
                    QuizOption(id="A", text="Understanding underlying definitions and inverse operations"),
                    QuizOption(id="B", text="Memorizing answers without proofs"),
                    QuizOption(id="C", text="Ignoring units and signs"),
                    QuizOption(id="D", text="Assuming all variables are equal to 1"),
                ],
                correct_id="A",
                explanation="Deep comprehension comes from understanding definitions and how inverse operations balance equations.",
                hint="Focus on systematic problem solving.",
            ),
        ]

    selected = base_questions[:count]
    return QuizResponse(topic=topic, difficulty=difficulty, questions=selected)


def build_offline_flashcards(topic: str, difficulty: str, count: int) -> FlashcardResponse:
    """Offline rule-based fallback when neither Gemini nor OpenRouter is reachable."""
    t_lower = topic.lower()

    if "rational" in t_lower or "number" in t_lower:
        base_cards = [
            Flashcard(
                id=1,
                front="Rational Number Definition",
                back="Any number that can be expressed in the form p/q, where p and q are integers and q ≠ 0.",
                category="Concept",
            ),
            Flashcard(
                id=2,
                front="Closure Property",
                back="Rational numbers are closed under addition, subtraction, and multiplication (a + b, a - b, and a * b are all rational).",
                category="Rule",
            ),
            Flashcard(
                id=3,
                front="Additive Inverse",
                back="For any rational number a/b, its additive inverse is -a/b such that (a/b) + (-a/b) = 0.",
                category="Rule",
            ),
            Flashcard(
                id=4,
                front="Multiplicative Inverse (Reciprocal)",
                back="For a non-zero rational number a/b, its reciprocal is b/a such that (a/b) * (b/a) = 1. Note: 0 has no reciprocal.",
                category="Formula",
            ),
            Flashcard(
                id=5,
                front="Distributive Property",
                back="a/b * (c/d + e/f) = (a/b * c/d) + (a/b * e/f). Multiplication distributes over addition.",
                category="Formula",
            ),
        ]
    elif "linear" in t_lower or "equation" in t_lower or "algebra" in t_lower:
        base_cards = [
            Flashcard(
                id=1,
                front="Linear Equation in One Variable",
                back="An algebraic equation where the highest exponent of the variable is 1 (standard form: ax + b = c, a ≠ 0).",
                category="Concept",
            ),
            Flashcard(
                id=2,
                front="Golden Rule of Equations",
                back="Whatever mathematical operation you perform on the left-hand side, you MUST perform equally on the right-hand side.",
                category="Rule",
            ),
            Flashcard(
                id=3,
                front="Transposition Method",
                back="A term can be moved from one side to the other by changing its sign: positive becomes negative, multiplication becomes division.",
                category="Rule",
            ),
            Flashcard(
                id=4,
                front="Checking the Solution",
                back="Substitute the obtained value of x back into the original LHS and RHS to verify that LHS = RHS.",
                category="Example",
            ),
            Flashcard(
                id=5,
                front="Standard Linear Form",
                back="ax + b = 0  =>  x = -b / a",
                category="Formula",
            ),
        ]
    else:
        base_cards = [
            Flashcard(
                id=1,
                front=f"{topic}: Core Definition",
                back=f"The fundamental principle of {topic} relies on clear definitions, axioms, and step-by-step logic.",
                category="Concept",
            ),
            Flashcard(
                id=2,
                front=f"{topic}: Inverse Operations",
                back="Every mathematical operation has an inverse: addition ↔ subtraction, multiplication ↔ division, power ↔ root.",
                category="Rule",
            ),
            Flashcard(
                id=3,
                front=f"{topic}: Verification Strategy",
                back="Always plug your calculated values back into the initial premise to confirm mathematical consistency.",
                category="Example",
            ),
        ]

    selected = base_cards[:count]
    return FlashcardResponse(topic=topic, cards=selected)
