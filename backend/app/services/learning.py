import json

from app.rag.store import KnowledgeStore


def save_learning_record(
    question: str,
    mode: str,
    grounded: bool,
    citation_pages: list[int],
) -> None:
    store = KnowledgeStore()
    store.init()
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO learning_records (question, mode, grounded, citation_pages)
            VALUES (?, ?, ?, ?)
            """,
            (question, mode, int(grounded), json.dumps(citation_pages, ensure_ascii=False)),
        )
        conn.commit()


def list_learning_records(limit: int = 20) -> list[dict]:
    store = KnowledgeStore()
    store.init()
    with store.connect() as conn:
        rows = conn.execute(
            """
            SELECT id, question, mode, grounded, citation_pages, created_at
            FROM learning_records
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [_record_from_row(row) for row in rows]


def get_learning_summary() -> dict:
    store = KnowledgeStore()
    store.init()
    with store.connect() as conn:
        total = conn.execute("SELECT COUNT(*) AS count FROM learning_records").fetchone()["count"]
        grounded = conn.execute(
            "SELECT COUNT(*) AS count FROM learning_records WHERE grounded = 1"
        ).fetchone()["count"]
    return {
        "total_questions": int(total),
        "grounded_questions": int(grounded),
        "recent_records": list_learning_records(limit=8),
    }


def _record_from_row(row) -> dict:
    return {
        "id": row["id"],
        "question": row["question"],
        "mode": row["mode"],
        "grounded": bool(row["grounded"]),
        "citation_pages": json.loads(row["citation_pages"] or "[]"),
        "created_at": row["created_at"],
    }
