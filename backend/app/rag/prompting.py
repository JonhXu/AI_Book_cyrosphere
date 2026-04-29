def build_prompt(question: str, contexts: list[dict], mode: str) -> str:
    mode_instruction = {
        "classroom": "以课堂助教风格解释概念，语言清晰，适合本科生。",
        "review": "以考试复习导师风格回答，突出重点、易混点和记忆框架。",
        "homework_hint": "这是作业或练习相关问题。请优先给提示、思路和相关知识点，不要直接给完整答案。",
    }.get(mode, "以课堂助教风格解释概念，语言清晰，适合本科生。")

    context_text = "\n\n".join(
        f"[资料{idx + 1} | 页码: {item.get('page') or '未知'} | 章节: {item.get('chapter') or '未知'}]\n{item['text']}"
        for idx, item in enumerate(contexts)
    )

    return f"""请严格依据给定教材资料回答学生问题。

教学要求：
- {mode_instruction}
- 如果资料不足以支持结论，请明确说明“教材资料不足”。
- 不要编造教材中没有的信息。
- 回答末尾用简短文字提示主要依据来自哪些资料编号。

教材资料：
{context_text}

学生问题：
{question}
"""

