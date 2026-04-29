import math
import re
import unicodedata
from collections import Counter

import jieba

from app.rag.store import KnowledgeStore

DOMAIN_LEXICON = {
    "冰冻圈": ["cryosphere", "cryospheric", "ice", "snow", "frozen ground"],
    "冰冻圈科学": ["cryospheric science", "cryosphere"],
    "冰川": ["glacier", "glaciers", "glacial"],
    "冻土": ["frozen ground", "permafrost"],
    "多年冻土": ["permafrost"],
    "积雪": ["snow", "snow cover"],
    "海冰": ["sea ice", "arctic sea ice"],
    "冰盖": ["ice sheet", "ice sheets"],
    "冰架": ["ice shelf", "ice shelves"],
    "冰芯": ["ice core", "ice cores"],
    "气候": ["climate", "climatic"],
    "气候系统": ["climate system"],
    "全球变化": ["global change"],
    "全球变暖": ["global warming", "climate warming"],
    "水文": ["hydrology", "hydrological"],
    "水资源": ["water resources", "freshwater"],
    "反照率": ["albedo", "surface reflectivity"],
    "碳循环": ["carbon cycle"],
    "温室气体": ["greenhouse gases"],
    "遥感": ["remote sensing"],
    "雪线": ["snowline", "snow line"],
    "物质平衡": ["mass balance"],
    "组成": ["component", "components", "element", "elements", "classification"],
    "组成部分": ["component", "components", "element", "elements"],
    "包括": ["include", "includes", "including", "consist"],
    "重要": ["important", "importance", "role", "roles", "affect", "regulate"],
    "作用": ["role", "roles", "function", "functions", "affect", "regulate"],
    "影响": ["impact", "impacts", "affect", "effects"],
}


def tokenize(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", text).lower()
    chinese_tokens = [token.strip() for token in jieba.lcut(normalized) if token.strip()]
    latin_tokens = re.findall(r"[a-z][a-z-]{1,}", normalized)
    return chinese_tokens + latin_tokens


def retrieve_context(question: str, top_k: int = 5) -> list[dict]:
    store = KnowledgeStore()
    chunks = store.all_chunks()
    if not chunks:
        return []

    expanded_question = expand_query(question)
    query_tokens = tokenize(expanded_question)
    query_counter = Counter(query_tokens)
    scored = []

    for chunk in chunks:
        chunk_counter = Counter(chunk["tokens"])
        score = cosine_score(query_counter, chunk_counter)
        score = adjust_score(score, chunk["text"])
        if score > 0:
            scored.append({**chunk, "score": round(score, 4)})

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


def expand_query(question: str) -> str:
    expansions: list[str] = []
    for chinese_term, english_terms in DOMAIN_LEXICON.items():
        if chinese_term in question:
            expansions.extend(english_terms)
    if expansions:
        return f"{question} {' '.join(expansions)}"
    return question


def adjust_score(score: float, text: str) -> float:
    lowered = text.lower()
    if lowered.strip().startswith("questions") or "\nquestions\n" in lowered:
        score *= 0.55
    if "roles of cryosphere" in lowered or "components in cryosphere" in lowered:
        score *= 1.2
    return score


def cosine_score(left: Counter, right: Counter) -> float:
    common = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)
