from contextlib import closing
import sqlite3
import database


import pytest


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    # 1. 创建临时数据库路径
    test_db_path = tmp_path / "test_chat.db"

    # 2. 临时替换数据库模块的路径
    monkeypatch.setattr(database, "DB_PATH", test_db_path)

    # 3. 创建 messages 数据表
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

    # 4. 返回测试数据库路径，用于清理数据库
    return test_db_path

def test_save_and_get_messages(test_db):
    database.save_messages("test_user", "user", "你好")

    messages = database.get_messages("test_user")

    assert messages == [
        {"role": "user", "content": "你好"}
    ]

def test_clear_messages(test_db):
    # 1. 保存两条消息
    database.save_messages("test_user", "user", "你好")
    database.save_messages("test_user", "assistant", "你好！")

    # 2. 清空该用户的聊天记录
    database.clear_messages("test_user")

    # 3. 查询并检查结果
    messages = database.get_messages("test_user")

    assert messages == []


def test_user_messages_are_isolated(test_db):
    # 1. 两个用户分别保存自己的消息
    database.save_messages("user_001", "user", "我是用户001")
    database.save_messages("user_002", "user", "我是用户002")

    # 2. 分别查询两个用户的记录
    messages_001 = database.get_messages("user_001")
    messages_002 = database.get_messages("user_002")

    # 3. 验证用户只能查到自己的消息
    assert messages_001 == [
        {"role": "user", "content": "我是用户001"}
    ]

    assert messages_002 == [
        {"role": "user", "content": "我是用户002"}
    ]



def test_clear_messages_does_not_affect_other_users(test_db):
    # 1. 两个用户分别保存自己的消息
    database.save_messages("user_001", "user", "用户001的消息")
    database.save_messages("user_002", "user", "用户002的消息")

    # 2. 清空用户001的聊天记录
    database.clear_messages("user_001")

    # 3. 验证用户001的记录已清空
    assert database.get_messages("user_001") == []

    # 4. 验证用户002的记录仍然存在
    assert database.get_messages("user_002") == [
        {"role": "user", "content": "用户002的消息"}
    ]
