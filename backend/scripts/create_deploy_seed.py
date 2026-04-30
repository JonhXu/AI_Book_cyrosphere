from pathlib import Path
import shutil
import sqlite3
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_DIR))

from app.core.config import PROJECT_ROOT  # noqa: E402


SOURCE_DB = PROJECT_ROOT / "data" / "app.db"
TARGET_DB = PROJECT_ROOT / "data" / "seed" / "app.db"


def main() -> None:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(f"本地知识库不存在：{SOURCE_DB}")

    TARGET_DB.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_DB, TARGET_DB)

    with sqlite3.connect(TARGET_DB) as conn:
        conn.execute("DELETE FROM learning_records")
        conn.execute("DELETE FROM quiz_attempts")
        conn.commit()
        conn.execute("VACUUM")

    with sqlite3.connect(TARGET_DB) as conn:
        chunk_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        record_count = conn.execute("SELECT COUNT(*) FROM learning_records").fetchone()[0]
        attempt_count = conn.execute("SELECT COUNT(*) FROM quiz_attempts").fetchone()[0]

    print(f"已生成部署种子库：{TARGET_DB}")
    print(f"教材知识块：{chunk_count}")
    print(f"学习记录：{record_count}")
    print(f"测验记录：{attempt_count}")


if __name__ == "__main__":
    main()
