# AI Chat Assistant

一个基于大语言模型的网页聊天助手，支持 AI 流式输出、历史聊天记录管理和 RAG 知识库问答。

## 项目功能

- 支持用户发送问题，并调用大语言模型生成回答
- 支持普通聊天模式下的流式输出
- 支持 Markdown 渲染与代码高亮
- 支持聊天历史记录查询
- 支持清空聊天记录
- 支持自定义聊天背景与界面样式
- 支持 RAG 知识库问答，根据本地文档检索相关资料并生成回答
- 支持文本分块、向量编码和相似度检索

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