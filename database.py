
import sqlite3
from contextlib import contextmanager
from pathlib import Path


# 数据库文件放在 database.py 所在的文件夹
DB_PATH = Path(__file__).parent / "chat.db"


@contextmanager
def get_db():
    # 每次数据库操作都创建独立连接
    conn = sqlite3.connect(DB_PATH, timeout=10)

    try:
        yield conn
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


# 初始化数据库表
with get_db() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            role TEXT,
            content TEXT
        )
    """)


def save_messages(user_id, role, content):
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO messages
            (user_id, role, content)
            VALUES (?, ?, ?)
            """,
            (user_id, role, content)
        )

def save_conversation(user_id, question, answer):
    with get_db() as conn:
        conn.executemany(
            """
            INSERT INTO messages (user_id, role, content)
            VALUES (?, ?, ?)
            """,
            [
                (user_id, "user", question),
                (user_id, "assistant", answer),
            ]
        )

def get_messages(user_id):
    with get_db() as conn:
        cursor = conn.execute(
            """
            SELECT role, content
            FROM messages
            WHERE user_id = ?
            ORDER BY id ASC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

    messages = []

    for row in rows:
        messages.append({
            "role": row[0],
            "content": row[1]
        })

    return messages


def clear_messages(user_id):
    with get_db() as conn:
        conn.execute(
            """
            DELETE FROM messages
            WHERE user_id = ?
            """,
            (user_id,)
        )
