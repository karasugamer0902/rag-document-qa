from dotenv import load_dotenv
import os
from google import genai
import chromadb
from app.services.pdf_service import process_pdf
import time
from google.genai.errors import ClientError
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key
)

chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)

def get_embedding(text: str):
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents = text
    )
    return result.embeddings[0].values

def get_embedding_with_retry(text: str, max_retries=5):
    for attempt in range(max_retries):
        try:
            return get_embedding(text)

        except ClientError as e:
            if getattr(e, "status_code", None) == 429:
                wait_seconds = 60

                print(
                    f"Rate limit hit. "
                    f"等待 {wait_seconds} 秒後重試 "
                    f"({attempt + 1}/{max_retries})"
                )

                time.sleep(wait_seconds)

            else:
                raise

    raise RuntimeError("Embedding 重試次數已達上限")

#chroma_client.delete_collection(
#    name="ipas_ai_planner"
#)

ipas_collection = chroma_client.get_or_create_collection(
    name="ipas_ai_planner"
)
start_index = ipas_collection.count()
print(f"將從 chunk_{start_index} 開始")

chunks = process_pdf(
    "data/AI應用規劃師(中級)-學習指引-科目1人工智慧技術應用規劃_20251222101833.pdf"
)
for index, chunk in enumerate(chunks[start_index:], start=start_index):
    embedding = get_embedding_with_retry(chunk)
    ipas_collection.add(
        ids=[f"chunk_{index}"],
        documents=[chunk],
        embeddings=[embedding]
    )
    print(f"目前已有 {index+1}/{len(chunks)} 個 chunks")
print("iPAS Collection count:", ipas_collection.count())