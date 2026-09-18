from fastapi import FastAPI
from pydantic import BaseModel

from app.retriever import retrieve_documents
from app.answer_generator import build_context
from app.llm import generate_answer


app = FastAPI(
    title="Enterprise AI Knowledge Assistant",
    description="RAG-based Enterprise Knowledge Assistant",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Enterprise AI Knowledge Assistant API is running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    # Retrieve relevant documents
    documents = retrieve_documents(request.question)

    # Build context from retrieved documents
    context = build_context(documents)

    # Generate answer using Ollama
    answer = generate_answer(
        request.question,
        context
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": documents
    }