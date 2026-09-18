from app.retriever import retrieve_documents


query = "How many Privilege Leave days are employees entitled to?"
results = retrieve_documents(query)


print("\nRetrieved Documents:\n")

for i, result in enumerate(results, start=1):

    print(f"--- Result {i} ---")
    print(f"Source: {result['source']}")
    print(f"Page: {result['page']}")
    print(f"Text: {result['text']}")
    print()