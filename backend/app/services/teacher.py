from app.rag.store import KnowledgeStore
from app.services.learning import list_learning_records


def get_teacher_dashboard() -> dict:
    store = KnowledgeStore()
    store.init()
    with store.connect() as conn:
        chunk_count = conn.execute("SELECT COUNT(*) AS count FROM chunks").fetchone()["count"]
        total_questions = conn.execute("SELECT COUNT(*) AS count FROM learning_records").fetchone()[
            "count"
        ]
        grounded_questions = conn.execute(
            "SELECT COUNT(*) AS count FROM learning_records WHERE grounded = 1"
        ).fetchone()["count"]
        quiz_row = conn.execute(
            """
            SELECT COUNT(*) AS attempts, COALESCE(AVG(percent), 0) AS average_percent
            FROM quiz_attempts
            """
        ).fetchone()
        question_rows = conn.execute(
            """
            SELECT question
            FROM learning_records
            ORDER BY id DESC
            LIMIT 6
            """
        ).fetchall()

    grounded_rate = round(grounded_questions / total_questions * 100, 1) if total_questions else 0.0
    return {
        "chunk_count": int(chunk_count),
        "total_questions": int(total_questions),
        "grounded_rate": grounded_rate,
        "quiz_attempts": int(quiz_row["attempts"]),
        "average_quiz_percent": round(float(quiz_row["average_percent"]), 1),
        "frequent_questions": [row["question"] for row in question_rows],
        "recent_records": list_learning_records(limit=6),
    }
