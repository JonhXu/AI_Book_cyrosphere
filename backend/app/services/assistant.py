from app.models.schemas import AskRequest, AskResponse, Citation
from app.rag.deepseek import DeepSeekClient
from app.rag.prompting import build_prompt
from app.rag.retriever import retrieve_context
from app.services.learning import save_learning_record


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
    answer = await client.chat(prompt)

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
