from fastapi import FastAPI
from pydantic import BaseModel
from app.services.llm_service import generate_answer
app = FastAPI(
    title = "RAG project",
    description = "RAG project",
    version = "1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "OK"}

class ChatRequest(BaseModel):
    question: str

@app.post("/chat")
def chat(question: ChatRequest):
    answer = generate_answer(question.question)
    return {"answer": answer}