from fastapi import APIRouter

from app.models.schemas import (
    AskRequest,
    AskResponse,
    ChapterPlan,
    ConceptSet,
    IndexStatus,
    LearningSummary,
    Quiz,
    QuizResult,
    QuizSubmission,
    TeacherDashboard,
)
from app.services.assistant import answer_question
from app.services.content import get_chapter_plan, get_concept_set
from app.services.index_status import get_index_status
from app.services.learning import get_learning_summary
from app.services.quiz import get_quiz, grade_quiz
from app.services.teacher import get_teacher_dashboard

router = APIRouter()


@router.get("/index/status", response_model=IndexStatus)
def index_status() -> IndexStatus:
    return get_index_status()


@router.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    return await answer_question(request)


@router.get("/learning/summary", response_model=LearningSummary)
def learning_summary() -> LearningSummary:
    return get_learning_summary()


@router.get("/learning/chapters", response_model=ChapterPlan)
def learning_chapters() -> ChapterPlan:
    return get_chapter_plan()


@router.get("/learning/concepts", response_model=ConceptSet)
def learning_concepts() -> ConceptSet:
    return get_concept_set()


@router.get("/quiz/current", response_model=Quiz)
def current_quiz() -> Quiz:
    return get_quiz()


@router.post("/quiz/submit", response_model=QuizResult)
def submit_quiz(submission: QuizSubmission) -> QuizResult:
    return grade_quiz(submission.quiz_id, submission.answers)


@router.get("/teacher/dashboard", response_model=TeacherDashboard)
def teacher_dashboard() -> TeacherDashboard:
    return get_teacher_dashboard()
