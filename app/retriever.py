from app.vector_store import collection, embedding_model


def retrieve_documents(query, top_k=3):

    # Convert the user's question into an embedding
    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    ).tolist()

    # Search ChromaDB for the most similar chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    retrieved_documents = []

    for i in range(len(results["documents"][0])):

        retrieved_documents.append(
            {
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "page": results["metadatas"][0][i]["page"],
            }
        )

    return retrieved_documents