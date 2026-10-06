from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from pathlib import Path

from app.retriever import retrieve_documents
from app.reranker import rerank_documents

from app.answer_generator import build_context
from app.llm import generate_answer
from app.grounding_checker import check_grounding

from app.document_loader import load_pdf
from app.chunker import chunk_documents
from app.vector_store import add_documents


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="Enterprise AI Knowledge Assistant",
    description="RAG-based Enterprise Knowledge Assistant",
    version="2.0.0"
)


# =========================================================
# Request Schema
# =========================================================

class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the enterprise documents"
    )


# =========================================================
# Source Schema
# =========================================================

class Source(BaseModel):

    source: str

    page: int | str

    section: str = ""


# =========================================================
# Response Schema
# =========================================================

class AnswerResponse(BaseModel):

    question: str

    answer: str

    grounded: bool

    sources: list[Source]


# =========================================================
# Health Check
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Enterprise AI Knowledge Assistant API is running"
    }


# =========================================================
# Ask Question
# =========================================================

@app.post(
    "/ask",
    response_model=AnswerResponse
)
def ask_question(
    request: QuestionRequest
):

    try:

        # -------------------------------------------------
        # Step 1: Hybrid Retrieval
        # -------------------------------------------------

        retrieved_documents = retrieve_documents(
            request.question,
            top_k=10
        )

        if not retrieved_documents:

            raise HTTPException(
                status_code=404,
                detail="No relevant documents were found."
            )


        # -------------------------------------------------
        # Step 2: Cross-Encoder Re-ranking
        # -------------------------------------------------

        reranked_documents = rerank_documents(
            request.question,
            retrieved_documents,
            top_k=5
        )

        if not reranked_documents:

            raise HTTPException(
                status_code=404,
                detail="No relevant documents remained after re-ranking."
            )


        # -------------------------------------------------
        # Step 3: Build Context
        # -------------------------------------------------

        context = build_context(
            reranked_documents
        )


        # -------------------------------------------------
        # DEBUG: Show Context Sent to LLM
        # -------------------------------------------------

        print(
            "\n========== CONTEXT SENT TO LLM ==========\n"
        )

        print(context)

        print(
            "\n=========================================\n"
        )


        # -------------------------------------------------
        # Step 4: Generate Answer
        # -------------------------------------------------

        generated_answer = generate_answer(
            request.question,
            context
        )


        # -------------------------------------------------
        # DEBUG: Show Generated Answer
        # -------------------------------------------------

        print(
            "\n========== GENERATED ANSWER ==========\n"
        )

        print(generated_answer)

        print(
            "\n======================================\n"
        )


        # -------------------------------------------------
        # Step 5: Grounding Check
        # -------------------------------------------------

        grounded = check_grounding(
            request.question,
            generated_answer,
            context
        )


        # -------------------------------------------------
        # DEBUG: Show Grounding Result
        # -------------------------------------------------

        print(
            "\n========== GROUNDING RESULT ==========\n"
        )

        print(
            f"Grounded: {grounded}"
        )

        print(
            "\n======================================\n"
        )


        # -------------------------------------------------
        # Step 6: Safe Fallback
        # -------------------------------------------------

        if not grounded:

            answer = (
                "I could not find enough information "
                "in the provided documents."
            )

        else:

            answer = generated_answer


        # -------------------------------------------------
        # Step 7: Build Unique Sources
        # -------------------------------------------------

        sources = []

        seen_sources = set()


        for document in reranked_documents:

            source_name = document.get(
                "source",
                "Unknown"
            )

            page = document.get(
                "page",
                "Unknown"
            )

            section = document.get(
                "section",
                ""
            )


            source_key = (
                source_name,
                page
            )


            if source_key in seen_sources:

                continue


            seen_sources.add(
                source_key
            )


            sources.append(
                Source(
                    source=source_name,
                    page=page,
                    section=section
                )
            )


        # -------------------------------------------------
        # Step 8: Return Response
        # -------------------------------------------------

        return AnswerResponse(
            question=request.question,
            answer=answer,
            grounded=grounded,
            sources=sources
        )


    except HTTPException:

        raise


    except Exception as error:

        print(
            f"API Error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An internal error occurred "
                "while processing the question."
            )
        )


# =========================================================
# Background Document Ingestion
# =========================================================

def ingest_documents():

    try:

        data_folder = Path(
            "data/documents/raw"
        )


        pdf_files = list(
            data_folder.glob("*.pdf")
        )


        if not pdf_files:

            print(
                "No PDF files found for ingestion."
            )

            return


        print(
            f"Starting background ingestion "
            f"of {len(pdf_files)} PDF files..."
        )


        # -------------------------------------------------
        # Load PDF pages
        # -------------------------------------------------

        all_documents = []


        for pdf_file in pdf_files:

            print(
                f"Loading: {pdf_file.name}"
            )


            pages = load_pdf(
                str(pdf_file)
            )


            print(
                f"Pages loaded: {len(pages)}"
            )


            all_documents.extend(
                pages
            )


        print(
            f"Total pages loaded: "
            f"{len(all_documents)}"
        )


        # -------------------------------------------------
        # Create chunks
        # -------------------------------------------------

        chunks = chunk_documents(
            all_documents
        )


        print(
            f"Total chunks created: "
            f"{len(chunks)}"
        )


        # -------------------------------------------------
        # Store in ChromaDB
        # -------------------------------------------------

        number_added = add_documents(
            chunks
        )


        print(
            f"Successfully stored "
            f"{number_added} chunks in ChromaDB."
        )


        print(
            "Background ingestion completed successfully."
        )


    except Exception as error:

        print(
            f"Background ingestion failed: {error}"
        )


# =========================================================
# Ingestion Endpoint
# =========================================================

@app.post("/ingest")
def start_ingestion(
    background_tasks: BackgroundTasks
):

    background_tasks.add_task(
        ingest_documents
    )


    return {
        "message": (
            "Document ingestion started "
            "in the background."
        )
    }