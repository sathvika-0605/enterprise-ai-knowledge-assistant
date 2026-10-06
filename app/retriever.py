import re

from rank_bm25 import BM25Okapi

from app.vector_store import collection, embedding_model
# ---------------------------------------------------------
# Load all documents from the V2 ChromaDB collection
# ---------------------------------------------------------

all_data = collection.get(
    include=["documents", "metadatas"]
)

documents = all_data["documents"]
metadatas = all_data["metadatas"]


# ---------------------------------------------------------
# Tokenizer for BM25
# ---------------------------------------------------------

def tokenize(text):
    """
    Convert text into lowercase tokens for BM25 keyword search.
    """

    return re.findall(
        r"\b\w+\b",
        text.lower()
    )


# Create tokenized corpus
tokenized_documents = [
    tokenize(document)
    for document in documents
]


# Create BM25 index
bm25 = BM25Okapi(
    tokenized_documents
)


# ---------------------------------------------------------
# Hybrid Retrieval
# ---------------------------------------------------------

def retrieve_documents(query, top_k=5):
    """
    Retrieve documents using both:

    1. ChromaDB vector search
    2. BM25 keyword search

    Results are merged using Reciprocal Rank Fusion (RRF).
    """

    # =====================================================
    # STEP 1: VECTOR SEARCH
    # =====================================================

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    vector_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k * 2, len(documents))
    )

    vector_ids = vector_results["ids"][0]


    # =====================================================
    # STEP 2: BM25 KEYWORD SEARCH
    # =====================================================

    query_tokens = tokenize(query)

    bm25_scores = bm25.get_scores(
        query_tokens
    )

    # Sort documents by BM25 score
    bm25_ranked_indices = sorted(
        range(len(bm25_scores)),
        key=lambda index: bm25_scores[index],
        reverse=True
    )

    bm25_ranked_indices = bm25_ranked_indices[
        :min(top_k * 2, len(documents))
    ]


    # =====================================================
    # STEP 3: CREATE RANK MAPS
    # =====================================================

    vector_rank = {}

    for rank, chunk_id in enumerate(vector_ids, start=1):
        vector_rank[chunk_id] = rank


    bm25_rank = {}

    for rank, index in enumerate(
        bm25_ranked_indices,
        start=1
    ):

        chunk_id = all_data["ids"][index]

        bm25_rank[chunk_id] = rank


    # =====================================================
    # STEP 4: RECIPROCAL RANK FUSION
    # =====================================================

    # RRF formula:
    #
    # score = 1 / (60 + rank)
    #
    # A document appearing in both searches
    # receives a higher combined score.

    rrf_scores = {}

    all_chunk_ids = set(
        vector_rank.keys()
    ).union(
        bm25_rank.keys()
    )

    for chunk_id in all_chunk_ids:

        score = 0

        if chunk_id in vector_rank:

            score += 1 / (
                60 + vector_rank[chunk_id]
            )

        if chunk_id in bm25_rank:

            score += 1 / (
                60 + bm25_rank[chunk_id]
            )

        rrf_scores[chunk_id] = score


    # Sort by combined RRF score
    ranked_chunk_ids = sorted(
        rrf_scores,
        key=rrf_scores.get,
        reverse=True
    )


    # Keep final top_k results
    ranked_chunk_ids = ranked_chunk_ids[
        :top_k
    ]


    # =====================================================
    # STEP 5: BUILD FINAL RESULTS
    # =====================================================

    # Map chunk ID → document index
    id_to_index = {
        all_data["ids"][index]: index
        for index in range(len(all_data["ids"]))
    }

    retrieved_documents = []

    for chunk_id in ranked_chunk_ids:

        index = id_to_index[chunk_id]

        metadata = metadatas[index]

        retrieved_documents.append(
            {
                "text": documents[index],

                "source": metadata.get(
                    "source",
                    "Unknown"
                ),

                "page": metadata.get(
                    "page",
                    "Unknown"
                ),

                "section": metadata.get(
                    "section",
                    ""
                ),

                "document_type": metadata.get(
                    "document_type",
                    "general_document"
                ),

                "chunk_id": metadata.get(
                    "chunk_id",
                    chunk_id
                ),

                "retrieval_score": round(
                    rrf_scores[chunk_id],
                    6
                ),
            }
        )


    return retrieved_documents