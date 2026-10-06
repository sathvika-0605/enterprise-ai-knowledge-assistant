from answer_generator import (
    build_context,
    build_citations
)

from retriever import retrieve_documents
from reranker import rerank_documents

from llm import generate_answer

from grounding_checker import check_grounding


# ---------------------------------------------------------
# User question
# ---------------------------------------------------------

question = "What is the company's maternity leave policy for international employees?"

# ---------------------------------------------------------
# STEP 1: Hybrid Retrieval
# ---------------------------------------------------------

retrieved_documents = retrieve_documents(
    question,
    top_k=10
)

print(
    f"\nRetrieved {len(retrieved_documents)} documents."
)


# ---------------------------------------------------------
# STEP 2: Cross-Encoder Re-ranking
# ---------------------------------------------------------

reranked_documents = rerank_documents(
    question,
    retrieved_documents,
    top_k=3
)

print(
    f"Selected {len(reranked_documents)} documents "
    "after re-ranking."
)


# ---------------------------------------------------------
# STEP 3: Build Context
# ---------------------------------------------------------

context = build_context(
    reranked_documents
)


# ---------------------------------------------------------
# STEP 4: Generate LLM Answer
# ---------------------------------------------------------

answer = generate_answer(
    question,
    context
)


# ---------------------------------------------------------
# STEP 5: Grounding Check
# ---------------------------------------------------------

is_grounded = check_grounding(
    question,
    answer,
    context
)


print(
    f"Grounding Check: "
    f"{'SUPPORTED' if is_grounded else 'NOT_SUPPORTED'}"
)


# ---------------------------------------------------------
# STEP 6: Handle Unsupported Answer
# ---------------------------------------------------------

if not is_grounded:

    answer = (
        "I could not find enough information "
        "in the provided documents."
    )


# ---------------------------------------------------------
# STEP 7: Build Source Citations
# ---------------------------------------------------------

citations = build_citations(
    reranked_documents
)


# ---------------------------------------------------------
# STEP 8: Display Final Response
# ---------------------------------------------------------

print("\n" + "=" * 60)

print("\nFINAL ANSWER:\n")

print(answer)

print("\nSOURCES:\n")

for citation in citations:
    print(f"- {citation}")

print("\n" + "=" * 60)