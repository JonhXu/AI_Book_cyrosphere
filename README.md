# 冰冻圈科学课堂虚拟助教

面向高校本科生的《冰冻圈科学概论》AI 辅助教学软件。系统以教材为权威知识源，通过检索增强生成（RAG）提供可溯源的概念解释、课堂答疑、复习辅助和作业提示。

## 当前目标

第一版先实现本地 MVP：

1. 解析《冰冻圈科学-秦大河.pdf》
2. 构建本地教材知识库
3. 提供基于教材出处的问答 API
4. 提供学生端 Web UI
5. 作业类问题默认提示优先，不直接给完整答案

## 项目结构

```text
backend/       FastAPI 后端与 RAG 服务
frontend/      React 学生端 UI
data/          原始教材、处理结果和索引
docs/          项目文档
```

## 配置

复制后端环境变量模板：

```bash
cp backend/.env.example backend/.env
```

然后在 `backend/.env` 中填写 DeepSeek API Key。

## 本地运行

安装后端依赖：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
```

建立教材知识库：

```bash
.venv/bin/python backend/scripts/index_book.py
```

启动本地软件：

```bash
.venv/bin/python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

浏览器访问：

```text
http://127.0.0.1:8000
```

## 当前 MVP 状态

- 已解析教材 PDF。
- 已建立 SQLite 本地教材知识库。
- 当前知识库包含 1384 个教材知识块。
- 已实现中文问题到英文教材的轻量双语关键词检索。
- 已实现 FastAPI 问答接口。
- 已实现无需前端构建工具的本地学生端 UI。
- React/Vite 版本前端代码已预留在 `frontend/`，后续安装 npm 后可升级。

## GitHub Pages 静态访问

`docs/` 目录是 GitHub Pages 静态发布版本。它可以通过 `https://<username>.github.io/<repo>/` 公网访问。

注意：GitHub Pages 不能运行 FastAPI 后端，也不能安全保存 DeepSeek API Key。因此静态页面可公网打开，但完整 AI 问答、学习记录、测验刷新和教师端统计需要另行部署后端 API。
