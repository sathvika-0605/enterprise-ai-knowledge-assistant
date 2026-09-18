from app.retriever import retrieve_documents
from app.answer_generator import build_context
from app.llm import generate_answer


question = "What is the company's travel reimbursement policy?"
# Retrieve relevant documents
documents = retrieve_documents(question)


print("\nRetrieved Documents:\n")

for i, document in enumerate(documents, start=1):
    print(f"--- Result {i} ---")
    print(f"Source: {document['source']}")
    print(f"Page: {document['page']}")
    print(f"Text: {document['text']}")
    print()


# Build context
context = build_context(documents)


print("\nContext sent to LLM:\n")
print(context)


# Generate final answer
answer = generate_answer(question, context)


print("\nFinal Answer:\n")
print(answer)