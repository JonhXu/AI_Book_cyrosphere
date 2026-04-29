import random

from app.rag.store import KnowledgeStore

QUIZZES = {
    "cryosphere-basics": {
        "id": "cryosphere-basics",
        "title": "冰冻圈科学基础小测",
        "description": "面向第一章与基础概念的课堂即时测验。",
        "questions": [
            {
                "id": "q1",
                "type": "single_choice",
                "prompt": "冰冻圈的主要组成部分不包括哪一项？",
                "options": ["冰盖和山地冰川", "积雪和海冰", "多年冻土和季节冻土", "平流层臭氧"],
                "answer": "平流层臭氧",
                "explanation": "教材将冰冻圈组成聚焦于冰、雪、冻土等固态水圈要素，平流层臭氧不属于冰冻圈组成部分。",
            },
            {
                "id": "q2",
                "type": "single_choice",
                "prompt": "为什么说冰冻圈是气候变化的天然指示器？",
                "options": [
                    "因为冰冻圈对气候变化非常敏感",
                    "因为冰冻圈完全不受气候影响",
                    "因为冰冻圈只存在于南极",
                    "因为冰冻圈不能记录环境变化",
                ],
                "answer": "因为冰冻圈对气候变化非常敏感",
                "explanation": "教材指出冰冻圈对气候变化敏感，因此其变化可反映气候系统的波动。",
            },
            {
                "id": "q3",
                "type": "single_choice",
                "prompt": "冰雪高反照率主要影响的是哪一类过程？",
                "options": ["地表能量平衡", "板块俯冲速度", "地核温度", "太阳黑子周期"],
                "answer": "地表能量平衡",
                "explanation": "冰雪高反照率会改变地表吸收和反射太阳辐射的比例，从而影响地表能量平衡。",
            },
            {
                "id": "q4",
                "type": "single_choice",
                "prompt": "课堂助教在回答教材依据不足的问题时，应该优先怎么做？",
                "options": ["明确说明教材依据不足", "编造一个看似合理的答案", "忽略教材来源", "只给网络泛泛答案"],
                "answer": "明确说明教材依据不足",
                "explanation": "本系统强调权威教材溯源，教材依据不足时应明确提示，而不是编造。",
            },
        ],
    },
    "cryosphere-processes": {
        "id": "cryosphere-processes",
        "title": "冰冻圈过程与反馈小测",
        "description": "聚焦冰冻圈形成、物理性质、气候反馈和圈层相互作用。",
        "questions": [
            {
                "id": "q1",
                "type": "single_choice",
                "prompt": "冰冻圈对气候系统的调节作用主要与哪组性质有关？",
                "options": ["高反照率、相变潜热、低导热性", "高盐度、强火山活动、低纬度", "强磁性、强酸性、高人口密度", "板块运动、地震波、地核热量"],
                "answer": "高反照率、相变潜热、低导热性",
                "explanation": "教材强调冰雪高反照率、相变潜热和低导热性等性质使冰冻圈能调节气候。",
            },
            {
                "id": "q2",
                "type": "single_choice",
                "prompt": "活动层通常指什么？",
                "options": ["多年冻土区上部季节性冻结和融化的土层", "海洋最深处的沉积层", "冰芯中的火山灰层", "平流层中的臭氧层"],
                "answer": "多年冻土区上部季节性冻结和融化的土层",
                "explanation": "活动层是多年冻土区对季节和气候变化响应非常敏感的近地表层。",
            },
            {
                "id": "q3",
                "type": "single_choice",
                "prompt": "冰冻圈与水圈相互作用最直接体现在哪类问题中？",
                "options": ["径流变化与水资源", "恒星形成", "火山岩浆分异", "城市交通拥堵"],
                "answer": "径流变化与水资源",
                "explanation": "冰川、积雪和冻土变化会影响径流过程和区域水资源。",
            },
            {
                "id": "q4",
                "type": "single_choice",
                "prompt": "冰芯记录常用于研究什么？",
                "options": ["过去气候与环境变化", "现代股票价格", "地球自转速度的每日变化", "城市建筑高度"],
                "answer": "过去气候与环境变化",
                "explanation": "冰芯中的同位素、气泡和化学成分可用于重建历史气候环境。",
            },
        ],
    },
    "cryosphere-application": {
        "id": "cryosphere-application",
        "title": "冰冻圈影响与应用小测",
        "description": "面向灾害、工程、适应和可持续发展主题。",
        "questions": [
            {
                "id": "q1",
                "type": "single_choice",
                "prompt": "冰冻圈变化对社会经济影响最相关的是哪一项？",
                "options": ["水资源、灾害风险和寒区工程稳定性", "文字字体选择", "太阳系行星命名", "网络协议版本"],
                "answer": "水资源、灾害风险和寒区工程稳定性",
                "explanation": "教材第 9 章关注冰冻圈变化对社会经济、灾害和工程建设的影响。",
            },
            {
                "id": "q2",
                "type": "single_choice",
                "prompt": "冰湖溃决属于哪类问题？",
                "options": ["冰冻圈灾害风险", "海洋潮汐发电", "臭氧层修复", "大气电离层扰动"],
                "answer": "冰冻圈灾害风险",
                "explanation": "冰湖溃决是冰冻圈变化背景下重要的山地灾害类型之一。",
            },
            {
                "id": "q3",
                "type": "single_choice",
                "prompt": "野外观测在冰冻圈科学中的作用是什么？",
                "options": ["获取过程数据并支撑模型和机理研究", "替代所有理论学习", "只用于旅游记录", "只用于绘制行政区划"],
                "answer": "获取过程数据并支撑模型和机理研究",
                "explanation": "教材第 10 章强调观测和测量方法对冰冻圈科学发展的支撑作用。",
            },
            {
                "id": "q4",
                "type": "single_choice",
                "prompt": "面对冰冻圈变化，适应策略应优先依据什么？",
                "options": ["监测数据、风险评估和区域差异", "单一经验判断", "完全忽视长期变化", "只考虑短期经济收益"],
                "answer": "监测数据、风险评估和区域差异",
                "explanation": "冰冻圈适应与可持续发展需要建立在监测、评估和区域情境判断之上。",
            },
        ],
    },
}


def get_quiz(quiz_id: str | None = None) -> dict:
    quiz = QUIZZES[quiz_id] if quiz_id else random.choice(list(QUIZZES.values()))
    return {
        "id": quiz["id"],
        "title": quiz["title"],
        "description": quiz["description"],
        "questions": [
            {
                "id": item["id"],
                "type": item["type"],
                "prompt": item["prompt"],
                "options": item["options"],
            }
            for item in quiz["questions"]
        ],
    }


def grade_quiz(quiz_id: str, answers: dict[str, str]) -> dict:
    quiz = QUIZZES[quiz_id]
    items = []
    score = 0
    for question in quiz["questions"]:
        selected = answers.get(question["id"], "")
        correct = selected == question["answer"]
        if correct:
            score += 1
        items.append(
            {
                "question_id": question["id"],
                "correct": correct,
                "correct_answer": question["answer"],
                "explanation": question["explanation"],
            }
        )

    total = len(quiz["questions"])
    percent = round(score / total * 100, 1) if total else 0.0
    _save_quiz_attempt(quiz_id=quiz_id, score=score, total=total, percent=percent)
    return {"quiz_id": quiz_id, "score": score, "total": total, "percent": percent, "items": items}


def _save_quiz_attempt(quiz_id: str, score: int, total: int, percent: float) -> None:
    store = KnowledgeStore()
    store.init()
    with store.connect() as conn:
        conn.execute(
            """
            INSERT INTO quiz_attempts (quiz_id, score, total, percent)
            VALUES (?, ?, ?, ?)
            """,
            (quiz_id, score, total, percent),
        )
        conn.commit()
