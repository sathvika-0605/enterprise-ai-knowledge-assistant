import ollama


def generate_answer(question, context):

    prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Answer the question using the information in the CONTEXT.

Important instructions:
- Use the context to answer the question.
- Do not add information that is not in the context.
- If the context contains a specific number, use that number.
- If multiple rules are relevant, explain them separately.
- If the answer is not present in the context, say:
  "I could not find this information in the provided documents."
- Include the source document and page number.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    return response["message"]["content"]