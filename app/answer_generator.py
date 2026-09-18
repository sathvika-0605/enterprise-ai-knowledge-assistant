from app.retriever import retrieve_documents


def build_context(documents):
    context = ""

    for i, document in enumerate(documents, start=1):

        context += f"""
Source: {document['source']}
Page: {document['page']}

Content:
{document['text']}

---
"""

    return context


def prepare_answer_prompt(question):

    documents = retrieve_documents(question)

    context = build_context(documents)

    prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Answer the user's question using ONLY the information provided
in the retrieved company policy documents.

If the answer is not available in the documents, say:
"I could not find this information in the provided documents."

Do not make up information.

User Question:
{question}

Retrieved Documents:
{context}

Provide a clear and concise answer.
Mention the source document and page number when relevant.
"""

    return prompt