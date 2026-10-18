from fastapi import FastAPI
from ai import chat as ai_chat, chat_stream
from pydantic import BaseModel
from database import clear_messages, get_messages, save_messages
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import time
from rag import answer_question

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],

)

class ChatRequest(BaseModel):
    user_id: str#user id
    question: str#question from user

class ClearRequest(BaseModel):
    user_id: str#user id

@app.post("/clear")#api endpoint
def clear_api(request: ClearRequest):#fastapi function #request must be a string
    clear_messages(request.user_id)#call the clear_messages function
    return {
        "message": "聊天记录已清空"#return the message to the user
        }

@app.post("/chat")#api endpoint
def chat_api(request: ChatRequest):#fastapi function #request must be a string

    answer = ai_chat(
        request.user_id,
        request.question
    )
    
    return {
        "answer": answer#return the answer to the user
        }

@app.get("/history/{user_id}")
def history(user_id:str):

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
    # 保存用户问题
    save_messages(
        request.user_id,
        "user",
        request.question
    )

    # 检索知识库并生成回答
    answer = answer_question(request.question)

    # 保存 AI 回答
    save_messages(
        request.user_id,
        "assistant",
        answer
    )

    # 返回答案给前端
    return {
        "answer": answer
    }