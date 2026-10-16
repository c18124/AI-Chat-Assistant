from openai import OpenAI
from config import API_KEY, MODEL
from database import get_messages, save_messages

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com"
    )

def chat(user_id, question):
    messages = get_messages(user_id)

    messages.append({
        "role": "user",
        "content": question
    })

    save_messages(user_id, "user", question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    answer = response.choices[0].message.content

    save_messages(user_id, "assistant", answer)

    return answer




def chat_stream(user_id, question):
    messages = get_messages(user_id)

    messages.append({
        "role": "user",
        "content": question
    })

    save_messages(user_id, "user", question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True
    )

    answer = ""

    try:
        for chunk in response:
            content = chunk.choices[0].delta.content

            if content:
                answer += content
                yield content

    finally:
        if answer:
            save_messages(user_id, "assistant", answer)
    
