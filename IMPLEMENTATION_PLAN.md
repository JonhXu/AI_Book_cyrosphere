# 冰冻圈科学课堂虚拟助教实施计划

## 1. 项目定位

本项目要构建一个面向高校本科生的《冰冻圈科学概论》课堂虚拟助教。它不是通用聊天机器人，而是以权威教材为核心知识源，围绕课程学习、概念理解、教材溯源、练习反馈和教师管理构建的 AI 辅助教学软件。

核心目标：

- 回答必须尽量基于教材内容，并提供章节、页码或片段出处。
- 面向本科生学习过程，优先启发、解释、引导，而不是直接替学生完成作业。
- 教师可以控制知识来源、课程章节、问答边界和学习反馈。
- 系统具备 UI，最终可本地运行，也可部署为 Web 应用。

## 2. 技术栈

### 前端

- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui 或等价的轻量 UI 组件

### 后端

- Python
- FastAPI
- Pydantic
- Uvicorn

### 模型与 RAG

- LLM：DeepSeek API
- RAG 编排：先自研轻量 RAG 流程，必要时接入 LlamaIndex
- Embedding：优先 bge-m3 或其他中文/多语言 embedding 模型
- Reranker：bge-reranker-v2-m3，作为增强阶段加入

### 数据存储

- MVP 阶段：SQLite + 本地向量索引，便于快速跑通
- 第一版正式系统：PostgreSQL + pgvector
- 扩展阶段：Qdrant，用于多教材、多课程、高并发或更复杂混合检索

### 教材解析

- PyMuPDF 或 pdfplumber
- 保留 page、chapter、section、paragraph_id、source_text 等元数据

## 3. MVP 范围

第一阶段只做最关键的闭环：

1. 解析《冰冻圈科学-秦大河.pdf》
2. 将教材切分成带页码和章节信息的知识块
3. 生成 embedding 并建立可检索知识库
4. 提供后端问答 API
5. 调用 DeepSeek API 生成基于教材的回答
6. 前端提供学生问答界面
7. 回答展示引用来源
8. 当教材中没有足够依据时，明确提示“教材依据不足”

## 4. 产品功能分期

### Phase 0：工程准备

- 初始化项目目录
- 配置 Python 后端环境
- 配置 React 前端环境
- 添加 `.env.example`
- 添加基础 README

### Phase 1：教材知识库

- PDF 文本抽取
- 章节/页码识别
- 文本清洗
- 教材 chunk 切分
- 本地持久化知识块
- embedding 生成
- 向量检索

### Phase 2：RAG 问答

- 用户问题改写或规范化
- Top-K 教材片段召回
- 可选 rerank
- 构造教学型系统提示词
- 调用 DeepSeek API
- 返回答案、引用、置信提示

### Phase 3：学生端 UI

- 章节导航
- 问答界面
- 引用来源卡片
- “继续追问”体验
- “不要直接给答案，先提示我”模式
- 学习历史记录

### Phase 4：教师端

- 教材索引状态
- 高信问题统计
- 学生常见误区
- 章节学习进度
- 教师可编辑系统提示词
- 题目/测验管理

### Phase 5：教学增强

- 概念图谱
- 章节小测自动生成
- 学生答案诊断
- 错题与薄弱知识点推荐
- 图表解释与过程推演

### Phase 6：部署与评估

- Docker Compose
- PostgreSQL + pgvector 迁移
- RAG 命中率评估集
- 回答忠实度评估
- 教师试用反馈表

## 5. 推荐目录结构

```text
AI_Book_cyrosphere/
  backend/
    app/
      api/
      core/
      rag/
      services/
      models/
    scripts/
    tests/
    pyproject.toml
    .env.example
  frontend/
    src/
      components/
      pages/
      services/
      styles/
    package.json
  data/
    raw/
    processed/
    indexes/
  docs/
  IMPLEMENTATION_PLAN.md
```

## 6. 关键设计原则

- 教材优先：回答先检索教材，再生成。
- 可溯源：每次回答尽量附引用。
- 不知道就说不知道：教材依据不足时不能编造。
- 教学引导：作业类问题默认先给提示、思路、相关知识点。
- 可替换：DeepSeek、embedding、向量库都通过配置解耦。
- 先 MVP 后扩展：先跑通一条高质量链路，再做教师端和复杂功能。

## 7. 近期交互事项

需要确认：

- 教材 PDF 是否允许作为系统知识库进行本地解析和索引。
- 第一版是否只面向单机/局域网试用，还是直接考虑服务器部署。
- DeepSeek API Key 后续放在本地 `.env`，不写入代码仓库。
- 第一版回答风格：更像“课堂助教解释”，还是更像“考试复习导师”。
