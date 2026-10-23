AI Chat Assistant

一个基于大语言模型的网页聊天助手，使用 Python、FastAPI 和 SQLite 构建，支持 AI 流式输出、历史聊天记录管理和 RAG 知识库问答。

项目已实现主要功能，并使用 pytest 完成数据库及 API 接口的基础自动化测试。

项目功能

- 支持用户发送问题，并调用大语言模型生成回答
- 支持普通聊天模式下的流式输出
- 支持 Markdown 渲染与代码高亮
- 支持聊天历史记录查询和清空
- 支持不同用户的聊天记录管理
- 支持自定义聊天背景与界面样式
- 支持 RAG 知识库问答，根据本地文档检索相关资料并生成回答
- 支持文本分块、向量编码和相似度检索
- 支持基础 API 参数校验和自动化测试

技术栈

后端

- Python
- FastAPI
- Pydantic
- SQLite
- Uvicorn

前端

- HTML
- CSS
- JavaScript
- Markdown 渲染与代码高亮

大模型与 RAG

- DeepSeek API（通过 OpenAI 兼容接口调用）
- Sentence Transformers
- BAAI/bge-small-zh-v1.5
- 基于向量相似度的文本检索

测试与工程化

- pytest
- FastAPI TestClient
- HTTPX
- pytest fixture
- monkeypatch
- SQLite 临时测试数据库
- Git / GitHub

项目结构

AI-Chat-Assistant/
├── images/
│   └── background.png
├── knowledge_base/
│   ├── project_intro.txt
│   └── python_notes.txt
├── tests/
│   ├── test_api.py
│   └── test_database.py
├── ai.py
├── api.py
├── config.py
├── database.py
├── index.html
├── main.py
├── rag.py
├── requirements.txt
├── README.md
└── .gitignore

主要文件说明：

- "ai.py"：大模型 API 调用与流式聊天
- "api.py"：FastAPI 接口、请求参数校验
- "database.py"：SQLite 聊天记录管理
- "rag.py"：RAG 知识库检索与问答
- "index.html"：前端聊天界面
- "tests/test_api.py"：API 接口自动化测试
- "tests/test_database.py"：数据库自动化测试

".env" 和 "chat.db" 为本地运行文件，不提交到 GitHub。

环境准备

- Python 3.13（当前开发测试环境）
- Conda 或其他 Python 虚拟环境工具
- DeepSeek API Key

安装依赖

建议先创建并激活 Python 虚拟环境，然后在项目根目录执行：

python -m pip install -r requirements.txt

运行自动化测试还需要安装：

python -m pip install pytest httpx

环境变量配置

在项目根目录创建 ".env" 文件，填写：

DEEPSEEK_API_KEY=你的DeepSeek_API_Key

如果 "config.py" 中还定义了其他环境变量，请根据实际配置填写。

安全提示： 不要将真实 API Key、".env" 文件或本地聊天数据库提交到公开仓库。

启动后端

在项目根目录执行：

uvicorn api:app --reload

启动后，访问 FastAPI 自动生成的接口文档：

http://127.0.0.1:8000/docs

使用方式

1. 启动 FastAPI 后端服务。
2. 在浏览器中打开 "index.html"。
3. 选择普通聊天模式或 RAG 知识库问答模式。
4. 输入问题并查看 AI 回答。
5. 使用历史记录和清空功能管理聊天记录。

RAG 工作流程

1. 加载 "knowledge_base/" 中的文本文件。
2. 将文档切分为多个文本块。
3. 使用 Sentence Transformers 将文本块转换为向量。
4. 将用户问题转换为向量，并计算与文本块的相似度。
5. 选取相关文本作为参考上下文。
6. 将问题和检索结果发送给大语言模型。
7. 返回生成的回答，并保存聊天记录。

自动化测试

项目使用 pytest 和 FastAPI TestClient 进行基础自动化测试，目前包含 13 个测试用例。

数据库测试（4 项）

- 消息保存与查询
- 聊天记录清空
- 不同用户的消息隔离
- 清空一个用户的记录不会影响其他用户

API 接口测试（9 项）

- 历史聊天记录查询
- 清空聊天记录接口
- 普通聊天接口
- 空问题参数校验
- 超长问题参数校验
- 空用户 ID 参数校验
- RAG 问答接口及消息保存
- 流式聊天接口返回内容
- 流式聊天接口空问题校验

测试设计

- 使用 "pytest fixture" 统一准备测试环境。
- 使用 "tmp_path" 创建临时 SQLite 测试数据库，隔离真实聊天记录。
- 使用 "monkeypatch" 模拟大模型及 RAG 函数，避免测试依赖真实 API 请求。
- 使用 "assert" 检查 HTTP 状态码、JSON 响应及数据库操作结果。

运行全部测试

在项目根目录执行：

python -m pytest -v

最近一次本地验证结果：

13 passed

说明当前编写的 13 个测试场景均已通过，不代表所有潜在问题均已覆盖。

## 技术栈

### 后端
- Python
- FastAPI
- Pydantic
- SQLite

### 前端
- HTML
- CSS
- JavaScript
- Markdown 渲染与代码高亮

### 大模型与 RAG
- DeepSeek API（通过 OpenAI 兼容接口调用）
- Sentence Transformers
- BAAI/bge-small-zh-v1.5
- 基于向量相似度的文本检索

## 项目结构

```text
MAX1/
├── images/
│   └── background.png
├── knowledge_base/
│   ├── project_intro.txt
│   └── python_notes.txt
├── ai.py
├── api.py
├── config.py
├── database.py
├── index.html
├── rag.py
├── requirements.txt
├── .env
└── .gitignore
```

## 环境准备

- Python
- Conda 或其他 Python 虚拟环境工具
- DeepSeek API Key

## 安装依赖

建议先激活自己的 Python 环境，再执行：

```bash
pip install -r requirements.txt
```

## 环境变量配置

在项目根目录创建 `.env` 文件，并按照 `config.py` 实际读取的变量名填写 DeepSeek API Key 和模型配置。

不要将真实 API Key 提交到 Git 仓库。

在项目根目录创建 `.env` 文件，填写：

DEEPSEEK_API_KEY=你的DeepSeek_API_Key

请将示例值替换为自己的真实 API Key，不要将真实密钥提交到 Git 仓库。
## 启动后端

在项目根目录运行：

```bash
uvicorn api:app --reload
```

启动后，可以通过以下地址访问 FastAPI 接口文档：

http://127.0.0.1:8000/docs

## 使用方式

1. 启动 FastAPI 后端服务。
2. 在浏览器中打开 `index.html`。
3. 选择普通聊天模式或 RAG 知识库问答模式。
4. 输入问题并查看 AI 回答。
5. 使用历史记录和清空功能管理聊天记录。

## RAG 工作流程

1. 加载知识库中的文本文件。
2. 将文档切分为多个文本块。
3. 使用 Embedding 模型将文本块转换为向量。
4. 将用户问题转换为向量。
5. 根据向量相似度检索相关文本块。
6. 将检索结果作为参考资料交给大语言模型生成回答。

## 数据存储

项目使用 SQLite 保存普通聊天模式下的用户问题和 AI 回答。

RAG 模式用于检索知识库文档，并根据检索结果生成回答。

## 安全说明

- `.env` 文件不应提交到版本控制系统。
- 不要公开真实 API Key。
- `chat.db` 等运行时数据文件按项目的 `.gitignore` 规则处理。