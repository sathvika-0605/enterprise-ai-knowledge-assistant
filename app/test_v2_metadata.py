from vector_store import collection


# Get a few documents from the V2 collection
results = collection.get(
    limit=15,
    include=["documents", "metadatas"]
)


print(f"Total documents in V2 collection: {collection.count()}")

print("\n========== SAMPLE V2 CHUNKS ==========\n")

for index in range(len(results["documents"])):

    print(f"--- Chunk {index + 1} ---")

    print("Text:")
    print(results["documents"][index][:300])

    print("\nMetadata:")
    print(results["metadatas"][index])

    print("\n" + "=" * 60)