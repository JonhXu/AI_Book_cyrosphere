from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.core.config import settings
from app.rag.retriever import tokenize
from app.rag.store import KnowledgeStore


def main() -> None:
    try:
        import fitz
    except ImportError as exc:
        raise SystemExit("缺少 PyMuPDF，请先安装 backend/requirements.txt 中的依赖。") from exc

    pdf_path = settings.book_pdf_path.resolve()
    if not pdf_path.exists():
        raise SystemExit(f"找不到教材 PDF：{pdf_path}")

    doc = fitz.open(pdf_path)
    chunks: list[dict] = []
    current_chapter: str | None = None

    for page_index, page in enumerate(doc, start=1):
        text = clean_text(page.get_text("text"))
        if not text:
            continue

        chapter = detect_chapter(text) or current_chapter
        current_chapter = chapter

        for idx, chunk_text in enumerate(split_text(text)):
            chunk_id = f"p{page_index:04d}-{idx:03d}"
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "page": page_index,
                    "chapter": chapter,
                    "section": None,
                    "text": chunk_text,
                    "tokens": tokenize(chunk_text),
                }
            )

    store = KnowledgeStore()
    store.replace_chunks(chunks)
    print(f"已建立教材知识库：{len(chunks)} 个知识块，来源：{pdf_path}")


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u3000", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def detect_chapter(text: str) -> str | None:
    match = re.search(r"(第[一二三四五六七八九十百\d]+章\s*[^\n]{2,40})", text)
    if match:
        return match.group(1).strip()
    return None


def split_text(text: str, max_chars: int = 900, overlap: int = 120) -> list[str]:
    paragraphs = [item.strip() for item in re.split(r"\n+", text) if item.strip()]
    chunks: list[str] = []
    buffer = ""

    for paragraph in paragraphs:
        candidate = f"{buffer}\n{paragraph}".strip() if buffer else paragraph
        if len(candidate) <= max_chars:
            buffer = candidate
            continue
        if buffer:
            chunks.append(buffer)
        if len(paragraph) > max_chars:
            chunks.extend(split_long_text(paragraph, max_chars=max_chars, overlap=overlap))
            buffer = ""
        else:
            buffer = paragraph

    if buffer:
        chunks.append(buffer)

    return chunks


def split_long_text(text: str, max_chars: int, overlap: int) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = max(0, end - overlap)
    return chunks


if __name__ == "__main__":
    main()
