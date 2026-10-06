from retriever import retrieve_documents
from reranker import rerank_documents


query = "How many registers are employers required to maintain under the Labour Codes?"


print("\n========== HYBRID RETRIEVAL ==========\n")

retrieved_documents = retrieve_documents(
    query,
    top_k=10
)

print(f"Retrieved: {len(retrieved_documents)} documents")


print("\n========== CROSS-ENCODER RE-RANKING ==========\n")

reranked_documents = rerank_documents(
    query,
    retrieved_documents,
    top_k=5
)


for index, result in enumerate(reranked_documents, start=1):

    print(f"\n--- RESULT {index} ---")

    print(f"Source: {result['source']}")
    print(f"Page: {result['page']}")
    print(f"Section: {result['section']}")
    print(f"Re-ranker Score: {result['reranker_score']}")

    print("\nTEXT:")
    print(result["text"])

    print("\n" + "=" * 70)