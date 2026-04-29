from app.models.schemas import AskRequest, AskResponse, Citation
from app.rag.deepseek import DeepSeekClient, DeepSeekError
from app.rag.prompting import build_prompt
from app.rag.retriever import retrieve_context
from app.services.learning import save_learning_record


def _fallback_answer(question: str, contexts: list[dict], reason: str) -> str:
    points = []
    for item in contexts[:3]:
        text = " ".join(item["text"].split())
        if len(text) > 160:
            text = f"{text[:160]}..."
        page = item.get("page")
        chapter = item.get("chapter") or "教材相关章节"
        source = f"{chapter}"
        if page is not None:
            source = f"{source}，第 {page} 页"
        points.append(f"- {source}：{text}")

    joined_points = "\n".join(points)
    return (
        f"DeepSeek 当前未能稳定返回（{reason}），我先根据《冰冻圈科学概论》教材检索片段给出临时回答。\n\n"
        f"你的问题是：{question}\n\n"
        "教材依据显示：\n"
        f"{joined_points}\n\n"
        "建议课堂学习时继续围绕这些教材出处追问，我会优先依据原教材片段进行解释。"
    )


async def answer_question(request: AskRequest) -> AskResponse:
    contexts = retrieve_context(request.question, top_k=request.top_k)
    grounded = len(contexts) > 0

    if not grounded:
        save_learning_record(
            question=request.question,
            mode=request.mode,
            grounded=False,
            citation_pages=[],
        )
        return AskResponse(
            answer="我暂时没有在教材知识库中找到足够依据。建议换一种问法，或先指定相关章节。",
            citations=[],
            grounded=False,
        )

    prompt = build_prompt(question=request.question, contexts=contexts, mode=request.mode)
    client = DeepSeekClient()
    try:
        answer = await client.chat(prompt)
    except DeepSeekError as exc:
        answer = _fallback_answer(
            question=request.question,
            contexts=contexts,
            reason=str(exc),
        )

    citations = [
        Citation(
            chunk_id=item["chunk_id"],
            page=item.get("page"),
            chapter=item.get("chapter"),
            section=item.get("section"),
            text=item["text"],
            score=item.get("score"),
        )
        for item in contexts
    ]

    save_learning_record(
        question=request.question,
        mode=request.mode,
        grounded=True,
        citation_pages=sorted({item.page for item in citations if item.page is not None}),
    )

    return AskResponse(answer=answer, citations=citations, grounded=grounded)
