from openai import OpenAI
from config import API_KEY, MODEL
from database import get_messages, save_messages

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com"
    )

# 只限制发给模型的历史，不删除数据库中的记录。
MAX_HISTORY_MESSAGES = 20
MAX_HISTORY_CHARS = 20000


def build_messages(user_id, question):
    history = get_messages(user_id)
    messages = []
    history_chars = 0

    # 从最新消息向前选取，保留连续的最近一段历史。
    for message in reversed(history[-MAX_HISTORY_MESSAGES:]):
        content_length = len(message["content"])

        if history_chars + content_length > MAX_HISTORY_CHARS:
            break

        messages.append(message)
        history_chars += content_length

    messages.reverse()

    # 避免截取后的上下文以孤立的 AI 回答开头。
    while messages and messages[0]["role"] == "assistant":
        messages.pop(0)

    # 当前问题始终保留，不计入历史消息的额度。
    messages.append({
        "role": "user",
        "content": question
    })

    return messages


def chat(user_id, question):
    messages = build_messages(user_id, question)

    save_messages(user_id, "user", question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    answer = response.choices[0].message.content

    save_messages(user_id, "assistant", answer)

    return answer




def chat_stream(user_id, question):
    messages = build_messages(user_id, question)

    save_messages(user_id, "user", question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )

    answer = ""

    try:
        for chunk in response:  #
            content = chunk.choices[0].delta.content

            if content:  # 如果有内容，则添加到回答中
                answer += content
                yield content

    finally:
        if answer:  # 如果回答不为空，则保存回答
            save_messages(user_id, "assistant", answer)
    
