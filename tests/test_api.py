import sqlite3
from contextlib import closing

import pytest
from fastapi.testclient import TestClient

import api
import database

client = TestClient(api.app)  # 创建 TestClient 实例

@pytest.fixture
def test_db(tmp_path, monkeypatch):
    # 1. 创建临时数据库路径
    test_db_path = tmp_path / "test_chat.db"

    # 2. 让数据库模块使用临时路径
    monkeypatch.setattr(database, "DB_PATH", test_db_path)

    # 3. 创建测试所需的数据表
    with closing(sqlite3.connect(test_db_path)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    role TEXT,
                    content TEXT
                )
            """)

    return test_db_path


def test_history_returns_user_messages(monkeypatch):  # 测试 /history 接口
    # 模拟数据库查询，避免读取真实聊天记录
    def fake_get_messages(user_id):
        return [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！"}
        ]

    monkeypatch.setattr(api, "get_messages", fake_get_messages)

    response = client.get("/history/test_user")

    assert response.status_code == 200

    assert response.json() == {
        "messages": [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "你好！"}
        ]
    }



def test_clear_messages(monkeypatch):
    called_users = []

    def fake_clear_messages(user_id):
        called_users.append(user_id)

    monkeypatch.setattr(api, "clear_messages", fake_clear_messages)

    response = client.post(
        "/clear",
        json={"user_id": "test_user"}
    )

    assert response.status_code == 200
    assert response.json() == {"message": "聊天记录已清空"}
    assert called_users == ["test_user"]


def test_chat_returns_ai_answer(monkeypatch):
    # 1. 模拟 AI 聊天函数
    def fake_ai_chat(user_id, question):
        return "你好！我是测试生成的回答。"

    monkeypatch.setattr(api, "ai_chat", fake_ai_chat)

    # 2. 向聊天接口发送请求
    response = client.post(
        "/chat",
        json={
            "user_id": "test_user",
            "question": "你好"
        }
    )

    # 3. 检查接口响应
    assert response.status_code == 200
    assert response.json() == {
        "answer": "你好！我是测试生成的回答。"
    }


def test_chat_rejects_empty_question():
    response = client.post(
        "/chat",
        json={
            "user_id": "test_user",
            "question": "   "
        }
    )

    assert response.status_code == 422

def test_chat_rejects_too_long_question():
    response = client.post(
        "/chat",
        json={
            "user_id": "test_user",
            "question": "a" * 4001
        }
    )

    assert response.status_code == 422

def test_chat_rejects_empty_user_id():  # 测试 /chat 接口的错误处理，空用户 ID 时的响应
    response = client.post(
        "/chat",
        json={
            "user_id": "   ",
            "question": "你好"
        }
    )

    assert response.status_code == 422


def test_rag_chat_returns_answer_and_saves_messages(
    monkeypatch, test_db
):  # 测试 /rag/chat 接口
    # 1. 模拟 RAG 问答函数
    def fake_answer_question(question):   # 模拟 RAG 问答函数
        return "这是模拟的知识库回答。"

    monkeypatch.setattr(api, "answer_question", fake_answer_question)

    # 2. 发送 RAG 问答请求
    response = client.post(
        "/rag/chat",
        json={
            "user_id": "rag_test_user",
            "question": "Python 是什么？"
        }
    )

    # 3. 检查接口响应
    assert response.status_code == 200
    assert response.json() == {
        "answer": "这是模拟的知识库回答。"
    }

    # 4. 检查用户问题和 AI 回答是否都被保存
    history_response = client.get("/history/rag_test_user")

    assert history_response.status_code == 200
    assert history_response.json()["messages"] == [
        {"role": "user", "content": "Python 是什么？"},
        {"role": "assistant", "content": "这是模拟的知识库回答。"}
    ]


def test_chat_stream_returns_streamed_text(monkeypatch):  # 测试 /chat/stream 接口
    # 1. 模拟流式聊天函数
    def fake_chat_stream(user_id, question):
        yield "你好，"
        yield "这是流式回答。"

    # 2. 替换真实的流式聊天函数
    monkeypatch.setattr(api, "chat_stream", fake_chat_stream)

    # 3. 发送流式聊天请求
    response = client.post(
        "/chat/stream",
        json={
            "user_id": "stream_test_user",
            "question": "你好"
        }
    )

    # 4. 检查状态码
    assert response.status_code == 200

    # 5. 检查最终收到的文本
    assert response.text == "你好，这是流式回答。"


def test_chat_stream_rejects_empty_question():  # 测试 /chat/stream 接口的错误处理，空问题时的响应
    response = client.post(
        "/chat/stream",
        json={
            "user_id": "stream_test_user",
            "question": "   "
        }
    )

    assert response.status_code == 422
