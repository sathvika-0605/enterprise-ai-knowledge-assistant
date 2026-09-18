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


# Create or load our collection
collection = chroma_client.get_or_create_collection(
    name="enterprise_documents"
)


def add_documents(chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = embedding_model.encode(
        texts,
        normalize_embeddings=True
    ).tolist()

    ids = [
        f"chunk_{index}"
        for index in range(len(chunks))
    ]

    metadatas = [
        {
            "source": chunk["source"],
            "page": chunk["page"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(chunks)