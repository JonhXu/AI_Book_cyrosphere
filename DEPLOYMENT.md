# 部署说明

## GitHub Pages 的边界

GitHub Pages 只能托管静态网页，适合发布本项目的前端页面，但不能直接运行：

- FastAPI 后端
- SQLite 教材知识库
- DeepSeek API 调用
- 教材 PDF 解析与索引脚本

因此，如果只使用 `https://<username>.github.io/<repo>/`，页面可以打开，但完整问答、测验记录、教师端统计等后端功能需要另一个可公网访问的 API 服务。

## 推荐公网方案

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

