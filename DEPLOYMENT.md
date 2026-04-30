# 部署说明

## GitHub Pages 的边界

GitHub Pages 只能托管静态网页，适合发布本项目的前端页面，但不能直接运行：

- FastAPI 后端
- SQLite 教材知识库
- DeepSeek API 调用
- 教材 PDF 解析与索引脚本

因此，如果只使用 `https://<username>.github.io/<repo>/`，页面可以打开，但完整问答、测验记录、教师端统计等后端功能需要另一个可公网访问的 API 服务。

## 当前固定公网方案：GitHub Pages + Render 后端

本项目已经加入 Render Blueprint 配置：

- `Dockerfile`：把 FastAPI 后端打包为容器服务。
- `render.yaml`：在 Render 上创建固定公网后端服务。
- `data/seed/app.db`：只包含 1384 个教材知识块，已清空本地学习记录和测验记录。

重要：当前 GitHub 仓库是公开仓库。`data/seed/app.db` 虽然不含学生学习记录，但包含教材文本切块，不应提交到公开仓库。固定后端部署建议使用一个私有后端仓库，或将数据库文件直接上传到学校服务器/云服务器。

部署后端后，Render 会提供固定 HTTPS 地址，通常形如：

```text
https://ai-book-cyrosphere-api.onrender.com
```

该地址不依赖本机电脑开机，也不会因为电脑睡眠或网络断开而失效。

### Render 部署步骤（推荐使用私有后端仓库）

1. 登录 Render。
2. 选择 `New +` -> `Blueprint`。
3. 连接私有后端 GitHub 仓库。

公开 GitHub Pages 仓库只负责前端页面。后端仓库应保持私有，并包含 `backend/`、`Dockerfile`、`render.yaml` 和 `data/seed/app.db`。

4. Render 会读取仓库根目录的 `render.yaml`，创建 `ai-book-cyrosphere-api` 服务。
5. 在 Render 服务环境变量中设置：

```text
DEEPSEEK_API_KEY=你的 DeepSeek API Key
```

6. 部署完成后访问：

```text
https://ai-book-cyrosphere-api.onrender.com/health
```

如果返回：

```json
{"status":"ok"}
```

说明固定后端已经上线。

7. 再访问：

```text
https://ai-book-cyrosphere-api.onrender.com/api/index/status
```

应返回教材知识库状态，包含 `chunk_count: 1384`。

8. 最后把公开前端仓库 `docs/config.js` 中的 `CRYOSPHERE_API_BASE` 设置为 Render 后端地址，并推送到 GitHub，GitHub Pages 就会长期连接该固定后端。

### 生成私有部署种子库

本地运行：

```bash
.venv/bin/python backend/scripts/create_deploy_seed.py
```

脚本会从 `data/app.db` 生成 `data/seed/app.db`，并清空学习记录和测验记录，只保留教材知识块。该文件默认被 `.gitignore` 排除，避免误传到公开仓库。

## 其他公网方案

### 方案 A：GitHub Pages + 云端后端

- 前端：部署 `backend/static/` 到 GitHub Pages
- 后端：部署 FastAPI 到 Render、Railway、Fly.io、云服务器或学校服务器
- 数据：使用云端 SQLite 卷、PostgreSQL 或 PostgreSQL + pgvector
- 前端 `API_BASE`：改为云端后端地址，例如 `https://your-api.example.com`

### 方案 B：单服务器部署

- 把前端静态文件和 FastAPI 后端一起部署到一台服务器
- 访问地址可以是学校域名、云服务器域名或反向代理后的 HTTPS 地址
- 这是最接近当前本地运行方式的完整部署方案

## 不应公开提交的文件

- `backend/.env`：包含 DeepSeek API Key
- `data/app.db`：本地教材索引与学习记录
- `冰冻圈科学-秦大河.pdf`：教材 PDF
- `.venv/`：本地 Python 虚拟环境

这些文件已经通过 `.gitignore` 排除。

`data/seed/app.db` 是专门用于云端部署的教材知识库种子文件，只包含教材知识块，不包含本地学习记录。它应只进入私有后端仓库或私有服务器环境。
