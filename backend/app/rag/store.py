import json
import sqlite3
from pathlib import Path

from app.core.config import settings


class KnowledgeStore:
    def __init__(self, db_path: Path | None = None) -> None:
        self.db_path = (db_path or settings.app_database_path).resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init(self) -> None:
        with self.connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    page INTEGER,
                    chapter TEXT,
                    section TEXT,
                    text TEXT NOT NULL,
                    tokens TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS learning_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    grounded INTEGER NOT NULL,
                    citation_pages TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS quiz_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quiz_id TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total INTEGER NOT NULL,
                    percent REAL NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def replace_chunks(self, chunks: list[dict]) -> None:
        self.init()
        with self.connect() as conn:
            conn.execute("DELETE FROM chunks")
            conn.executemany(
                """
                INSERT INTO chunks (chunk_id, page, chapter, section, text, tokens)
                VALUES (:chunk_id, :page, :chapter, :section, :text, :tokens)
                """,
                [
                    {
                        **chunk,
                        "tokens": json.dumps(chunk["tokens"], ensure_ascii=False),
                    }
                    for chunk in chunks
                ],
            )
            conn.commit()

    def all_chunks(self) -> list[dict]:
        self.init()
        with self.connect() as conn:
            rows = conn.execute("SELECT * FROM chunks").fetchall()
        return [
            {
                "chunk_id": row["chunk_id"],
                "page": row["page"],
                "chapter": row["chapter"],
                "section": row["section"],
                "text": row["text"],
                "tokens": json.loads(row["tokens"]),
            }
            for row in rows
        ]

    def count_chunks(self) -> int:
        self.init()
        with self.connect() as conn:
            row = conn.execute("SELECT COUNT(*) AS count FROM chunks").fetchone()
        return int(row["count"])
