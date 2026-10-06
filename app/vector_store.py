import chromadb
from sentence_transformers import SentenceTransformer


# Local embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Create a persistent ChromaDB client
chroma_client = chromadb.PersistentClient(
    path="chroma_db"
)


# Create or load V2 collection
collection = chroma_client.get_or_create_collection(
    name="enterprise_documents_v2"
)


def add_documents(chunks):

    # Extract text from chunks
    texts = [chunk["text"] for chunk in chunks]

    # Create embeddings
    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True
    ).tolist()

    # Create unique IDs for each chunk
    ids = [
        f"chunk_{index}"
        for index in range(len(chunks))
    ]

    # Store metadata for each chunk
    metadatas = [
        {
            "source": chunk.get("source", ""),
            "page": chunk.get("page", 0),
            "section": chunk.get("section", ""),
            "document_type": chunk.get("document_type", ""),
            "chunk_id": f"chunk_{index}",
        }
        for index, chunk in enumerate(chunks)
    ]

    # Add documents to ChromaDB
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(chunks)