# AI Chat Assistant

一个基于大语言模型（LLM）的 Web AI 聊天助手，使用 Python、FastAPI、SQLite 和原生前端技术构建，支持普通 AI 对话、流式输出、聊天历史管理以及 RAG 本地知识库问答。

本项目从前后端交互、数据库持久化、LLM API 调用到 RAG 检索问答均已实现，并使用 pytest 完成自动化测试，同时支持通过 Docker 容器化部署。

## 项目功能

- **AI 普通对话**：调用 DeepSeek API 生成 AI 回答，支持结合历史消息进行多轮对话。
- **流式输出**：通过后端流式接口逐步返回 AI 生成的内容。
- **聊天历史管理**：保存、查询和清空指定用户的聊天记录。
- **多用户记录隔离**：根据 user_id 区分不同用户的聊天记录。
- **Markdown 渲染**：支持 Markdown 格式展示和代码高亮。
- **自定义聊天界面**：支持聊天背景、消息气泡、时间戳、加载动画和错误提示。
- **RAG 知识库问答**：检索本地知识库中的相关资料，并结合检索结果生成回答。
- **文本分块与向量检索**：将知识文档切分为文本块，通过文本向量和相似度计算检索相关内容。
- **接口参数校验**：使用 Pydantic 校验请求参数，并处理异常请求。
- **自动化测试**：使用 pytest、FastAPI TestClient、HTTPX 和 monkeypatch 测试 API 与数据库逻辑。
- **Docker 部署**：使用 Dockerfile 和 Docker Compose 构建、启动和管理应用容器。

## 技术栈

### 后端开发

- Python
- FastAPI
- Pydantic
- Uvicorn
- SQLite
- OpenAI Python SDK（兼容 DeepSeek API）

### 前端开发

- HTML
- CSS
- JavaScript
- Fetch API
- Markdown 渲染
- highlight.js 代码高亮

### 大模型与 RAG

- DeepSeek API
- Sentence Transformers
- BAAI/bge-small-zh-v1.5
- 文本分块（Text Chunking）
- 文本向量化（Embedding）
- 向量相似度检索
- 基于检索结果的增强生成（RAG）

### 测试与工程化

- pytest
- FastAPI TestClient
- HTTPX
- pytest fixture
- monkeypatch
- 临时 SQLite 测试数据库
- Git / GitHub
- Docker
- Docker Compose

## 项目结构

```text
AI-Chat-Assistant/
├── images/
│   └── background.png
├── knowledge_base/
│   ├── project_intro.txt
│   └── python_notes.txt
├── tests/
│   ├── test_api.py
│   └── test_database.py
├── .dockerignore
├── .gitignore
├── .env
├── ai.py
├── api.py
├── config.py
├── database.py
├── Dockerfile
├── docker-compose.yml
├── index.html
├── main.py
├── rag.py
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

> 以上目录为项目主要文件示意，实际文件以仓库内容为准。`.env`、`chat.db` 等本地文件不应提交到公开仓库。

## 核心文件说明

| 文件 | 作用 |
|---|---|
| `api.py` | FastAPI 应用入口、HTTP 接口、参数校验及异常处理 |
| `ai.py` | 大模型 API 调用、普通聊天及流式响应逻辑 |
| `database.py` | SQLite 连接管理、聊天记录增删查及事务处理 |
| `rag.py` | 知识库加载、文本分块、向量化、相似度检索及问答 |
| `config.py` | 加载模型及 API 相关配置 |
| `index.html` | 前端聊天界面、交互逻辑及消息展示 |
| `tests/test_api.py` | API 接口自动化测试 |
| `tests/test_database.py` | 数据库操作自动化测试 |
| `requirements.txt` | 应用运行依赖 |
| `requirements-dev.txt` | 开发及测试依赖 |
| `Dockerfile` | 定义应用镜像构建步骤 |
| `docker-compose.yml` | 定义容器服务、端口和相关运行配置 |

## 环境准备

本地开发环境：

- Python 3.13（已使用的本地开发与测试环境）
- pip
- DeepSeek API Key

容器部署环境：

- Docker Desktop
- Docker Compose

## 本地运行

### 1. 克隆项目

```bash
git clone https://github.com/c18124/AI-Chat-Assistant.git
cd AI-Chat-Assistant
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

Windows PowerShell 激活环境：

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. 安装依赖

```bash
python -m pip install -r requirements.txt
```

安装开发和测试依赖：

```bash
python -m pip install -r requirements-dev.txt
```

如果测试依赖没有包含在开发依赖文件中，可单独安装：

```bash
python -m pip install pytest httpx
```

### 4. 配置环境变量

在项目根目录创建 `.env` 文件，根据 `config.py` 实际读取的变量名称填写 API 配置。

示例：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
```

请将示例值替换为自己的密钥，并确认模型名称、API Base URL 等配置与 `config.py` 的实际实现一致。

**安全注意：不要将真实 API Key 提交到 GitHub。**

### 5. 启动后端

在项目根目录执行：

```bash
uvicorn api:app --reload
```

启动成功后访问：

- API 文档：http://127.0.0.1:8000/docs
- OpenAPI Schema：http://127.0.0.1:8000/openapi.json

### 6. 打开前端

在浏览器中打开项目的 `index.html`，使用聊天界面与后端进行交互。

## API 接口

| 方法 | 路径 | 功能 |
|---|---|---|
| POST | `/chat` | 普通 AI 聊天 |
| POST | `/chat/stream` | 流式 AI 聊天 |
| GET | `/history/{user_id}` | 查询指定用户的聊天历史 |
| POST | `/clear` | 清空指定用户的聊天历史 |
| POST | `/rag/chat` | RAG 知识库问答 |

接口请求示例：

```json
{
  "user_id": "001",
  "question": "Python 是什么？"
}
```

普通聊天接口的响应示例：

```json
{
  "answer": "Python 是一种通用编程语言。"
}
```

以上内容仅为请求和响应格式示例，实际回答由模型生成。

## RAG 工作流程

RAG（Retrieval-Augmented Generation，检索增强生成）通过先检索相关资料，再将资料提供给大语言模型，帮助模型结合本地知识库回答问题。

本项目的主要流程如下：

1. 加载 `knowledge_base/` 目录中的知识文档。
2. 将文档切分为适当大小的文本块。
3. 使用 Sentence Transformers 将文本块转换为向量表示。
4. 将用户问题转换为向量。
5. 计算问题向量与文本块向量之间的相似度。
6. 检索相关文本块，并将其作为参考上下文。
7. 将用户问题与检索结果交给大语言模型生成回答。
8. 返回回答，并按照项目实际实现保存聊天记录。

RAG 可以让模型参考本地资料回答问题，但回答的准确性仍然受到知识库内容、检索效果及模型生成能力的影响。

## 自动化测试

项目使用 pytest 对数据库操作和 API 接口进行自动化测试。

### 测试覆盖范围

**数据库测试**

- 消息保存与查询。
- 聊天记录清空。
- 不同用户的消息隔离。
- 清空一个用户的记录不会影响其他用户。

**API 测试**

- 普通聊天请求与响应。
- 历史记录查询。
- 清空聊天记录。
- 请求参数校验。
- RAG 问答及聊天记录保存。
- 流式聊天响应。
- 大模型或 RAG 处理异常时的错误响应。

**测试设计**

- 使用 pytest fixture 准备测试环境。
- 使用临时 SQLite 数据库隔离测试数据。
- 使用 monkeypatch 模拟大模型及 RAG 函数，减少测试对真实外部服务的依赖。
- 使用断言验证 HTTP 状态码、JSON 响应和数据库结果。

### 运行测试

运行全部测试：

```bash
python -m pytest -q
```

仅运行 API 测试：

```bash
python -m pytest -q tests/test_api.py
```

最近一次记录的本地测试结果：

```text
Full test suite: 15 passed
API tests:       11 passed
```

以上为最近一次本地验证结果，重新运行测试后可获得当前代码对应的实际结果。自动化测试有助于发现回归问题，但不能保证覆盖所有潜在缺陷。

## Docker 部署

项目支持使用 Docker 将应用及运行依赖打包为镜像，并通过 Docker Compose 启动服务。

请确保 Docker Desktop 已启动，并且当前终端能够正常使用 Docker 命令。

### 1. 构建镜像

在包含 `Dockerfile` 和 `docker-compose.yml` 的项目根目录执行：

```bash
docker compose build
```

### 2. 启动服务

```bash
docker compose up -d
```

### 3. 查看容器状态

```bash
docker compose ps
```

确认应用容器处于运行状态，并检查端口映射是否正常。

### 4. 查看运行日志

```bash
docker compose logs --tail=50
```

需要持续观察日志时：

```bash
docker compose logs -f
```

按 `Ctrl+C` 可退出日志跟踪，不会自动停止后台容器。

### 5. 验证服务

浏览器访问：

http://127.0.0.1:8000/docs

通过 Swagger UI 测试 API 接口，确认服务能够正常响应。

### 6. 停止服务

```bash
docker compose down
```

此命令会停止并移除 Compose 管理的容器和网络。持久化数据是否保留取决于项目的卷挂载及数据存储配置。

> 注意：容器中的代码、依赖、环境变量和数据持久化行为取决于 `Dockerfile` 与 `docker-compose.yml` 的具体配置。修改代码后，如果需要将变更应用到容器，通常需要重新构建镜像并更新服务。

## 数据存储

项目使用 SQLite 保存聊天记录。数据库操作通过独立连接执行，并使用参数化 SQL 查询，降低 SQL 注入风险。

普通聊天与 RAG 聊天的具体保存行为以 `ai.py`、`api.py` 和 `database.py` 中的实际实现为准。

本地数据库文件 `chat.db` 不应直接提交到公开仓库。测试应优先使用独立的临时数据库，避免测试数据污染真实聊天记录。

## 安全说明

- 将 API Key 等敏感信息放在环境变量中，不要硬编码在源码中。
- 将 `.env`、`chat.db`、虚拟环境及测试缓存加入 `.gitignore` 或 `.dockerignore` 的适当规则中。
- 确认公开仓库中没有真实密钥、个人数据或其他敏感信息。
- 生产环境应限制 CORS 允许的来源，并根据实际需求配置身份认证、访问控制和请求频率限制。
- 当前项目主要用于学习、开发和作品展示；正式部署到公网前，还应完善鉴权、日志、监控及数据安全措施。

## 项目总结

本项目覆盖了一个 AI 应用从前端交互到后端服务、从数据库持久化到 RAG 检索问答，以及从自动化测试到 Docker 容器化部署的完整开发流程。

通过该项目实践了：

- FastAPI 接口设计与参数校验。
- 大语言模型 API 集成及流式响应。
- SQLite 数据持久化与事务管理。
- RAG 检索增强生成的基本实现。
- pytest 自动化测试与异常场景验证。
- Git/GitHub 版本管理。
- Docker 镜像构建与容器部署。

项目地址：[GitHub - AI-Chat-Assistant](https://github.com/c18124/AI-Chat-Assistant)
