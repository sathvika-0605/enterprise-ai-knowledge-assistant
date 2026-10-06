from sentence_transformers import CrossEncoder


# ---------------------------------------------------------
# Load Cross-Encoder model
# ---------------------------------------------------------

reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


# ---------------------------------------------------------
# Re-rank retrieved documents
# ---------------------------------------------------------

def rerank_documents(query, documents, top_k=3):
    """
    Re-rank documents using a Cross-Encoder.

    The Cross-Encoder receives:
        query + document

    and directly calculates how relevant
    the document is to the query.
    """

    if not documents:
        return []

    # Create query-document pairs
    pairs = [
        [
            query,
            document["text"]
        ]
        for document in documents
    ]

    # Calculate relevance scores
    scores = reranker_model.predict(pairs)

    # Add re-ranking score
    reranked_documents = []

    for document, score in zip(
        documents,
        scores
    ):

        document_copy = document.copy()

        document_copy["reranker_score"] = round(
            float(score),
            6
        )

        reranked_documents.append(
            document_copy
        )

    # Sort by Cross-Encoder score
    reranked_documents.sort(
        key=lambda document: document["reranker_score"],
        reverse=True
    )

    # Return best documents
    return reranked_documents[:top_k]