import sqlite3

conn = sqlite3.connect(
    "chat.db",
    check_same_thread=False#database name
    )

cursor = conn.cursor()

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS messages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    role TEXT,
    content TEXT
)
"""
)   

conn.commit()

def save_messages(user_id, role, content):

    cursor.execute(
    """
    INSERT INTO messages
    (user_id, role, content)
    VALUES (?, ?, ?)
    """,
    (user_id, role, content)
    )

    conn.commit()
    
def get_messages(user_id):

    cursor.execute(
    """
    SELECT role,content
    FROM messages
    WHERE user_id=?
    """,
    (user_id,)
    )


    rows = cursor.fetchall()


    messages=[]


    for row in rows:
        messages.append(
        {
            "role":row[0],
            "content":row[1]
        }
        )

    return messages

def clear_messages(user_id):
    cursor.execute(
    """
    DELETE FROM messages
    WHERE user_id=?
    """,
    (user_id,)
    )

    conn.commit()