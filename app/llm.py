import ollama


def generate_answer(question, context):
    """
    Generate an answer using only the retrieved enterprise
    document context.
    """

    prompt = f"""
You are an Enterprise AI Knowledge Assistant.

Answer the user's question using ONLY the information
provided in the CONTEXT.

IMPORTANT RULES:

1. Answer the question directly and clearly.

2. If the question asks "How many", "How much", "How many days",
   "How many weeks", or another numerical question, look carefully
   for an explicit numerical statement in the context.

3. When the context contains an explicit numerical answer,
   prefer that direct numerical statement over a detailed list
   or related information.

4. Example:
   If the context says:
   "registers have reduced from 84 to just 8"
   and the question asks:
   "How many registers are required?"
   answer:
   "8 registers."

5. If the question asks whether something is allowed and the
   context explicitly states that it is not allowed as a standard
   practice, answer that directly.

6. Do NOT refuse to answer when the relevant information is
   clearly present in the context.

7. Do NOT use outside knowledge.

8. Do NOT invent facts.

9. Small wording differences are acceptable.

10. Keep the answer focused on what the user asked.

11. Include the relevant source/page information when it is
    available in the context.

12. If the requested information genuinely cannot be found
    in the context, say:
    "I could not find this information in the provided documents."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    try:

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

        answer = response["message"]["content"].strip()

        print(
            "\n========== GENERATED ANSWER ==========\n"
        )

        print(answer)

        print(
            "\n======================================\n"
        )

        return answer

    except Exception as error:

        print(
            f"LLM generation error: {error}"
        )

        return (
            "I could not find this information "
            "in the provided documents."
        )