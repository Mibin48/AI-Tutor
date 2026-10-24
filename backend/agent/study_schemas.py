from typing import Optional
from pydantic import BaseModel, Field


class QuizOption(BaseModel):
    id: str = Field(description="Option identifier: A, B, C, or D")
    text: str = Field(description="Option text")


class QuizQuestion(BaseModel):
    id: int = Field(description="Question number starting from 1")
    question: str = Field(description="The question prompt")
    options: list[QuizOption] = Field(description="List of 4 multiple-choice options A, B, C, D")
    correct_id: str = Field(description="The key of the correct option: 'A', 'B', 'C', or 'D'")
    explanation: str = Field(description="Detailed step-by-step mathematical reasoning for why the answer is correct")
    hint: Optional[str] = Field(None, description="Optional subtle hint to assist the student")


class QuizRequest(BaseModel):
    topic: str = Field(default="Rational Numbers", description="Maths topic or concept")
    num_questions: int = Field(default=3, ge=1, le=10, description="Number of questions (1-10)")
    difficulty: str = Field(default="medium", description="Difficulty: easy, medium, or hard")
    provider: Optional[str] = Field(None, description="Optional override provider: gemini or openrouter")


class QuizResponse(BaseModel):
    topic: str
    difficulty: str
    questions: list[QuizQuestion]


class Flashcard(BaseModel):
    id: int = Field(description="Card index starting from 1")
    front: str = Field(description="Front of card: concept, key term, formula, or problem statement")
    back: str = Field(description="Back of card: definition, formula breakdown, or step-by-step explanation")
    category: str = Field(default="Concept", description="Category: Formula, Concept, Example, or Rule")


class FlashcardRequest(BaseModel):
    topic: str = Field(default="Rational Numbers", description="Maths topic or concept")
    num_cards: int = Field(default=5, ge=1, le=15, description="Number of flashcards (1-15)")
    difficulty: str = Field(default="medium", description="Difficulty: easy, medium, or hard")
    provider: Optional[str] = Field(None, description="Optional override provider: gemini or openrouter")


class FlashcardResponse(BaseModel):
    topic: str
    cards: list[Flashcard]
