from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    mode: str = Field(default="classroom", description="classroom, review, homework_hint")
    top_k: int = Field(default=5, ge=1, le=10)


class Citation(BaseModel):
    chunk_id: str
    page: int | None = None
    chapter: str | None = None
    section: str | None = None
    text: str
    score: float | None = None


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    grounded: bool


class IndexStatus(BaseModel):
    exists: bool
    chunk_count: int
    message: str


class LearningRecord(BaseModel):
    id: int
    question: str
    mode: str
    grounded: bool
    citation_pages: list[int]
    created_at: str


class LearningSummary(BaseModel):
    total_questions: int
    grounded_questions: int
    recent_records: list[LearningRecord]


class QuizQuestion(BaseModel):
    id: str
    type: str = "single_choice"
    prompt: str
    options: list[str]


class Quiz(BaseModel):
    id: str
    title: str
    description: str
    questions: list[QuizQuestion]


class QuizSubmission(BaseModel):
    quiz_id: str
    answers: dict[str, str]


class QuizResultItem(BaseModel):
    question_id: str
    correct: bool
    correct_answer: str
    explanation: str


class QuizResult(BaseModel):
    quiz_id: str
    score: int
    total: int
    percent: float
    items: list[QuizResultItem]


class ChapterItem(BaseModel):
    number: int
    title: str
    title_en: str
    pages: str
    summary: str
    learning_task: str
    question: str


class ChapterPlan(BaseModel):
    title: str
    description: str
    refresh_note: str
    chapters: list[ChapterItem]


class ConceptItem(BaseModel):
    title: str
    summary: str
    review_prompt: str
    question: str


class ConceptSet(BaseModel):
    title: str
    description: str
    concepts: list[ConceptItem]


class TeacherDashboard(BaseModel):
    chunk_count: int
    total_questions: int
    grounded_rate: float
    quiz_attempts: int
    average_quiz_percent: float
    frequent_questions: list[str]
    recent_records: list[LearningRecord]
