from retriever import retrieve_documents


# ---------------------------------------------------------
# Test Query
# ---------------------------------------------------------

query = "Can employees work from home?"

# ---------------------------------------------------------
# Run Hybrid Retrieval
# ---------------------------------------------------------

results = retrieve_documents(
    query,
    top_k=5
)


# ---------------------------------------------------------
# Display Results
# ---------------------------------------------------------

print("\n========== HYBRID SEARCH RESULTS ==========\n")

print(f"Query: {query}\n")

for i, result in enumerate(
    results,
    start=1
):

    print(f"--- Result {i} ---")

    print(
        f"Source: {result['source']}"
    )

    print(
        f"Page: {result['page']}"
    )

    print(
        f"Section: {result['section']}"
    )

    print(
        f"Document Type: {result['document_type']}"
    )

    print(
        f"Chunk ID: {result['chunk_id']}"
    )

    print(
        f"Retrieval Score: {result['retrieval_score']}"
    )

    print(
        f"Text:\n{result['text']}"
    )

    print(
        "\n" + "=" * 60 + "\n"
    )