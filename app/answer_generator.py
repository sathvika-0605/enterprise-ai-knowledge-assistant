from app.retriever import retrieve_documents
from app.reranker import rerank_documents


# ---------------------------------------------------------
# Build context from re-ranked documents
# ---------------------------------------------------------

def build_context(documents):
    """
    Build the context that will be sent to the LLM.

    Each chunk includes:
    - source file
    - page number
    - section
    - document type
    """

    context = ""

    for i, document in enumerate(
        documents,
        start=1
    ):

        context += f"""
Document {i}

Source: {document['source']}
Page: {document['page']}
Section: {document.get('section', '')}
Document Type: {document.get('document_type', '')}

Content:
{document['text']}

---
"""

    return context


# ---------------------------------------------------------
# Build source citations
# ---------------------------------------------------------

def build_citations(documents):
    """
    Create source citations from the retrieved documents.
    """

    citations = []

    seen = set()

    for document in documents:

        source = document.get(
            "source",
            "Unknown"
        )

        page = document.get(
            "page",
            "Unknown"
        )

        citation = (
            f"{source}, Page {page}"
        )

        if citation not in seen:

            citations.append(
                citation
            )

            seen.add(citation)

    return citations


# ---------------------------------------------------------
# Prepare LLM prompt
# ---------------------------------------------------------

def prepare_answer_prompt(question):
    """
    Retrieve, re-rank and prepare the final
    context for the LLM.
    """

    # =====================================================
    # STEP 1: HYBRID RETRIEVAL
    # =====================================================

    retrieved_documents = retrieve_documents(
        question,
        top_k=10
    )


    # =====================================================
    # STEP 2: CROSS-ENCODER RE-RANKING
    # =====================================================

    reranked_documents = rerank_documents(
        question,
        retrieved_documents,
        top_k=3
    )


    # =====================================================
    # STEP 3: BUILD CONTEXT
    # =====================================================

    context = build_context(
        reranked_documents
    )


    # =====================================================
    # STEP 4: BUILD CITATIONS
    # =====================================================

    citations = build_citations(
        reranked_documents
    )

    citation_text = "\n".join(
        f"- {citation}"
        for citation in citations
    )


    # =====================================================
    # STEP 5: CREATE LLM PROMPT
    # =====================================================

    prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Your task is to answer the user's question using ONLY
the information provided in the retrieved company documents.

IMPORTANT RULES:

1. Do not use outside knowledge.
2. Do not invent or assume information.
3. If the retrieved documents do not contain enough
   information to answer the question, say:

   "I could not find enough information in the
   provided documents."

4. Keep the answer clear and concise.
5. Use the retrieved content as the source of truth.
6. Do not mention information that is not supported
   by the retrieved documents.
7. Include the relevant source file and page number
   in the answer.

User Question:
{question}

Retrieved Documents:
{context}

Available Sources:
{citation_text}

Answer:
"""

    return prompt