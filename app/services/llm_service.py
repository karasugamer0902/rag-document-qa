from dotenv import load_dotenv
import os
from google import genai
import chromadb

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

ipas_collection = chroma_client.get_or_create_collection(
    name="ipas_ai_planner"
)

def get_embedding(text: str):
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents = text
    )
    return result.embeddings[0].values

print("iPAS Collection count:", ipas_collection.count())

def retrieve_context(question: str) -> str:
    question_embedding = get_embedding(question)

    results = ipas_collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    context = "\n\n".join(results["documents"][0])
    distances = results["distances"][0]
    print("Question:", question)
    print("Distances:", distances)

    for index, document in enumerate(results["documents"][0]):
        print(f"\n----- Rank {index + 1} -----")
        print(document)
    #if distances > 0.5:
    #    return "沒有對應答案"
    return context
    
def generate_answer(question: str) -> str:
    context = retrieve_context(question)
    print("Retrieved context:", context)
    prompt = f"""請根據以下參考資料回答使用者的問題。
    參考資料：
    {context}
    
    使用者問題：
    {question}"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text