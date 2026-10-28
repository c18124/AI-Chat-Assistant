from fastapi import FastAPI, HTTPException
from ai import chat as ai_chat, chat_stream
from typing import Annotated
from pydantic import BaseModel, StringConstraints
from database import (
    clear_messages,
    get_messages,
    save_messages,
    save_conversation,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import time
from rag import answer_question
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)

logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],

)

# 先去除首尾空白，再检查长度；保留问题内部的换行和空格。
UserId = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100, strict=True),
]
Question = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=4000, strict=True),
]


class ChatRequest(BaseModel):
    user_id: UserId
    question: Question

class ClearRequest(BaseModel):
    user_id: UserId

@app.post("/clear")#api endpoint
def clear_api(request: ClearRequest):#fastapi function #request must be a string
    clear_messages(request.user_id)#call the clear_messages function
    return {
        "message": "聊天记录已清空"#return the message to the user
        }

@app.post("/chat")
def chat_api(request: ChatRequest):
    logger.info("普通聊天请求开始处理")

    try:
        answer = ai_chat(
            request.user_id,
            request.question
        )

        return {
            "answer": answer
        }

    except Exception as exc:
        logger.exception("普通聊天请求处理失败")

        raise HTTPException(
            status_code=500,
            detail="服务器处理请求失败，请稍后重试"
        ) from exc

@app.get("/history/{user_id}")
def history(user_id: UserId):

    messages = get_messages(user_id)

    return {
        "messages": messages
    }


@app.post("/chat/stream")
def chat_stream_api(request: ChatRequest):

    generator = chat_stream(
        request.user_id,
        request.question
    )

    return StreamingResponse(
        generator,
        media_type="text/plain; charset=utf-8"
    )

@app.post("/rag/chat")
def rag_chat_api(request: ChatRequest):
    logger.info("RAG 问答请求开始处理")

    try:
        # 先检索知识库并生成回答
        answer = answer_question(request.question)

        # 回答生成成功后，一次性保存完整对话
        save_conversation(
            request.user_id,
            request.question,
            answer
        )

        # 返回答案给前端
        return {
            "answer": answer
        }

    except Exception as exc:
        logger.exception("RAG 问答请求处理失败")

        raise HTTPException(
            status_code=500,
            detail="知识库问答处理失败，请稍后重试"
        ) from exc