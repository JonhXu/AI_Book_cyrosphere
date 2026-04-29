from app.rag.store import KnowledgeStore


def get_index_status():
    store = KnowledgeStore()
    chunk_count = store.count_chunks()
    exists = chunk_count > 0
    message = "教材知识库已建立" if exists else "尚未建立教材知识库，请先运行索引脚本"
    return {"exists": exists, "chunk_count": chunk_count, "message": message}

