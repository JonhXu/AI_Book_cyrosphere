import random

CHAPTERS = [
    {
        "number": 1,
        "title": "冰冻圈与冰冻圈科学",
        "title_en": "Cryosphere and Cryospheric Science",
        "pages": "第 14 页起",
        "summary": "介绍冰冻圈的定义、研究对象、学科形成过程，以及冰冻圈在全球变化和社会发展中的作用。",
        "question": "什么是冰冻圈科学？它的主要研究对象和学科意义是什么？",
    },
    {
        "number": 2,
        "title": "冰冻圈的分类与地理分布",
        "title_en": "Classification and Geographical Distribution of Cryosphere",
        "pages": "第 46 页起",
        "summary": "系统梳理陆地冰冻圈、海洋冰冻圈和大气冰冻圈的分类体系，并介绍各组成要素的全球分布。",
        "question": "冰冻圈各组成部分的分类和地理分布有什么特点？",
    },
    {
        "number": 3,
        "title": "冰冻圈的形成与发育",
        "title_en": "Formation and Development of the Cryosphere",
        "pages": "第 93 页起",
        "summary": "解释液态水冻结、固态水状态变化及不同冰冻圈要素形成、演化和发育的基本过程。",
        "question": "冰冻圈是如何形成和发育的？不同组成要素有什么差异？",
    },
    {
        "number": 4,
        "title": "冰冻圈的物理性质",
        "title_en": "Physical Properties of the Cryosphere",
        "pages": "第 118 页起",
        "summary": "介绍冰、雪、冻土、海冰等组成要素的热学、力学、光学和电磁性质，是理解过程机制的基础。",
        "question": "冰冻圈主要物理性质有哪些？这些性质为什么重要？",
    },
    {
        "number": 5,
        "title": "冰冻圈的化学特征",
        "title_en": "Chemical Characteristics of the Cryosphere",
        "pages": "第 152 页起",
        "summary": "聚焦冰川雪冰、冻土和海冰中的化学成分、空间分布及其对气候和环境变化研究的意义。",
        "question": "冰冻圈化学特征如何帮助理解气候与环境变化？",
    },
    {
        "number": 6,
        "title": "冰冻圈中的气候与环境记录",
        "title_en": "Climatic and Environmental Record in Cryosphere",
        "pages": "第 187 页起",
        "summary": "介绍冰芯、冻土、树轮和湖泊沉积等载体中的气候环境记录，用于重建过去变化。",
        "question": "冰冻圈中哪些载体可以保存气候与环境记录？它们各有什么特点？",
    },
    {
        "number": 7,
        "title": "不同时间尺度上的冰冻圈演化",
        "title_en": "Cryospheric Evolutions at Different Time Scales",
        "pages": "第 216 页起",
        "summary": "从地质时期到现代变化，讨论冰冻圈在不同时间尺度上的演化过程和驱动因素。",
        "question": "冰冻圈在不同时间尺度上的演化有什么主要特征？",
    },
    {
        "number": 8,
        "title": "冰冻圈与其他圈层的相互作用",
        "title_en": "Interactions Between Cryosphere and the Other Spheres",
        "pages": "第 261 页起",
        "summary": "讨论冰冻圈与大气圈、水圈、生物圈、岩石圈之间的相互作用和反馈机制。",
        "question": "冰冻圈如何与大气圈、水圈、生物圈和岩石圈相互作用？",
    },
    {
        "number": 9,
        "title": "冰冻圈变化影响、适应与可持续发展",
        "title_en": "Cryosphere Change Impact, Adaptation and Sustainable Development",
        "pages": "第 323 页起",
        "summary": "介绍冰冻圈变化对社会经济、灾害风险、工程建设和可持续发展的影响及适应策略。",
        "question": "冰冻圈变化会对社会经济和可持续发展造成哪些影响？",
    },
    {
        "number": 10,
        "title": "冰冻圈科学野外观测与测量",
        "title_en": "Field Observations and Measurements for Cryospheric Science",
        "pages": "第 372 页起",
        "summary": "介绍冰冻圈野外观测、实验测量、数据获取和技术方法，是课程实践能力的重要部分。",
        "question": "冰冻圈科学常用哪些野外观测与测量方法？",
    },
]

TASK_TEMPLATES = [
    "阅读本章后，用三句话说明“定义、过程、意义”三层内容。",
    "找出本章最容易混淆的两个概念，并说明它们的区别。",
    "用一张因果链条图概括本章的关键机制。",
    "列出本章能够支撑课堂讨论的三个教材依据。",
    "把本章内容转化为一道课堂讨论题和一道选择题。",
]

CONCEPT_POOL = [
    {
        "title": "冰冻圈",
        "summary": "地球系统中以冰、雪、冻土等固态水形式存在的圈层，是气候变化研究的重要对象。",
        "review_prompt": "复习时要同时记住组成要素、空间分布和气候意义。",
        "question": "冰冻圈包括哪些组成部分？",
    },
    {
        "title": "反照率反馈",
        "summary": "冰雪反射太阳辐射，冰雪减少会降低反照率、增强地表吸热，进一步推动变暖。",
        "review_prompt": "重点理解“冰雪减少 -> 吸热增加 -> 继续变暖”的正反馈链条。",
        "question": "冰雪反照率反馈如何影响气候系统？",
    },
    {
        "title": "多年冻土",
        "summary": "长期处于冻结状态的土体，对生态、水文、工程建设和碳循环均有重要影响。",
        "review_prompt": "注意区分多年冻土、季节冻土和活动层。",
        "question": "多年冻土退化会产生哪些环境影响？",
    },
    {
        "title": "活动层",
        "summary": "多年冻土区上部每年发生季节性冻结和融化的土层，是冻土变化的重要响应层。",
        "review_prompt": "把活动层厚度变化与气候变暖、工程稳定性联系起来理解。",
        "question": "活动层厚度变化为什么重要？",
    },
    {
        "title": "冰川物质平衡",
        "summary": "冰川积累与消融之间的收支关系，是判断冰川变化趋势的重要指标。",
        "review_prompt": "复习时围绕积累区、消融区和零平衡线组织知识。",
        "question": "冰川物质平衡如何反映冰川变化？",
    },
    {
        "title": "海冰",
        "summary": "海水冻结形成的冰体，影响海气交换、极地反照率和海洋环流过程。",
        "review_prompt": "注意海冰与冰架、冰山、陆地冰川的区别。",
        "question": "海冰变化为什么会影响极地气候？",
    },
    {
        "title": "冰芯记录",
        "summary": "冰芯保存了气泡、同位素和化学成分等信息，可用于重建过去气候与环境变化。",
        "review_prompt": "把冰芯看成气候环境信息的时间序列档案。",
        "question": "冰芯可以记录哪些气候环境信息？",
    },
    {
        "title": "冰冻圈灾害",
        "summary": "包括冰湖溃决、冰川跃动、冻融灾害、雪灾等，与气候变化和人类活动密切相关。",
        "review_prompt": "从触发因素、影响对象和风险管理三个角度复习。",
        "question": "冰冻圈变化会带来哪些灾害风险？",
    },
]


def get_chapter_plan() -> dict:
    offset = random.randrange(len(TASK_TEMPLATES))
    chapters = []
    for index, chapter in enumerate(CHAPTERS):
        chapters.append(
            {
                **chapter,
                "learning_task": TASK_TEMPLATES[(index + offset) % len(TASK_TEMPLATES)],
            }
        )
    return {
        "title": "《冰冻圈科学概论》章节学习路线",
        "description": "按教材 10 章组织学习，每次刷新会更新每章的课堂学习任务。",
        "refresh_note": "已生成新的章节学习任务。",
        "chapters": chapters,
    }


def get_concept_set() -> dict:
    concepts = random.sample(CONCEPT_POOL, k=4)
    return {
        "title": "核心概念复习卡片",
        "description": "每次刷新抽取 4 个概念，适合课前预习、课后自测和课堂快速提问。",
        "concepts": concepts,
    }
