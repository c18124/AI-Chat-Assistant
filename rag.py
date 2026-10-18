from pathlib import Path
from sentence_transformers import SentenceTransformer
from ai import client, MODEL

# 获取知识库文件夹的路径
KNOWLEDGE_DIR = Path(__file__).parent / "knowledge_base"  # 获取当前文件的父目录


def load_txt(file_name: str) -> str:
    file_path = KNOWLEDGE_DIR / file_name   # 拼接文件路径

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()  # 读取文件内容

    return text


def split_text(text: str, chunk_size: int = 200, overlap: int = 30) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap 必须大于等于 0 且小于 chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = end - overlap

    return chunks


# if __name__ == "__main__":
#     content = load_txt("project_intro.txt")
#     chunks = split_text(content)

#     print(f"文档总字符数：{len(content)}")
#     print(f"切分后文本块数量：{len(chunks)}")

#     for i, chunk in enumerate(chunks, start=1):
#         print(f"\n--- Chunk {i} ---")
#         print(chunk)

def test_embedding():
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

    text = "SQLite 用于保存用户问题和 AI 回答。"

    vector = model.encode(text)

    print("原始文本：", text)
    print("向量类型：", type(vector))
    print("向量维度：", vector.shape)
    print("向量前 10 个数字：", vector[:10])

def retrieve_chunks(question, chunks, vectors, model, top_k=2):  # 检索相关文本
    # 1. 将用户的问题转换成向量
    query_vector = model.encode(   
        question,  
        normalize_embeddings=True
    )

    # 2. 计算问题与所有文本块的相似度
    scores = vectors @ query_vector

    # 3. 按相似度从高到低排列文本块的索引
    ranked_indices = sorted(
        range(len(chunks)),
        key=lambda i: scores[i],
        reverse=True  # 倒序排列
    )

    # 4. 取出最相关的 top_k 个文本块
    results = []

    for i in ranked_indices[:top_k]:
        results.append((chunks[i], float(scores[i])))

    return results


def generate_answer(question, retrieved_chunks):  # 生成 AI 的回答
    # 1. 将检索到的文本块整理成参考资料
    context = "\n\n".join(
        chunk for chunk, score in retrieved_chunks
    )

    # 2. 组织发给大模型的消息
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个基于参考资料回答问题的助手。"
                "请优先依据提供的参考资料回答。"
                "如果资料中没有相关信息，请明确说明，"
                "不要编造资料中不存在的事实。"
            )
        },
        {
            "role": "user",
            "content": (
                f"参考资料：\n{context}\n\n"
                f"用户问题：{question}"
            )
        }
    ]

    # 3. 调用 DeepSeek API
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    # 4. 提取 AI 的回答并返回
    answer = response.choices[0].message.content

    return answer


# 保存已经初始化的 RAG 数据
_rag_model = None
_rag_chunks = None
_rag_vectors = None


def initialize_rag():  # 初始化 RAG 数据
    global _rag_model, _rag_chunks, _rag_vectors

    # 如果已经初始化，就不重复加载
    if _rag_model is not None:  # 如果已经初始化，就不重复加载
        return

    # 1. 加载 Embedding 模型
    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

    # 2. 读取知识库文档
    content = load_txt("project_intro.txt")

    # 3. 将文档切分成文本块
    chunks = split_text(content)

    # 4. 将所有文本块转换成向量
    vectors = model.encode(
        chunks,
        normalize_embeddings=True
    )

    # 5. 将结果保存到模块级变量
    _rag_model = model
    _rag_chunks = chunks
    _rag_vectors = vectors


def answer_question(question: str) -> str:
    # 确保模型和知识库已经准备好
    initialize_rag()

    # 根据用户问题检索相关文本
    results = retrieve_chunks(
        question,
        _rag_chunks,
        _rag_vectors,
        _rag_model,
        top_k=2
    )

    # 根据检索结果生成最终回答
    answer = generate_answer(question, results)

    return answer



if __name__ == "__main__":
    question = "我的聊天记录使用什么数据库保存？"

    answer = answer_question(question)

    print("用户问题：", question)
    print("\n--- RAG 最终回答 ---")
    print(answer)
