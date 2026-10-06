import ollama
import re


# =========================================================
# Stopwords
# =========================================================

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "be", "been", "being",
    "to", "of", "for", "from", "in", "on", "at",
    "by", "with", "and", "or", "as",
    "this", "that", "these", "those",
    "it", "they", "them", "their",
    "there", "here",
    "can", "may", "must", "should",
    "do", "does", "did",
    "how", "many", "much",
    "what", "when", "where", "who",
    "according", "document", "section",
    "yes", "no"
}


# =========================================================
# Normalize text
# =========================================================

def normalize_text(text):

    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# Extract important words
# =========================================================

def get_content_words(text):

    normalized = normalize_text(text)

    words = normalized.split()

    content_words = []

    for word in words:

        if word in STOPWORDS:
            continue

        if len(word) <= 1:
            continue

        content_words.append(word)

    return content_words


# =========================================================
# Check whether answer is directly supported
# =========================================================

def direct_support_check(answer, context):

    normalized_answer = normalize_text(answer)
    normalized_context = normalize_text(context)


    # -----------------------------------------------------
    # 1. Check numbers
    # -----------------------------------------------------

    answer_numbers = re.findall(
        r"\b\d+(?:\.\d+)?\b",
        normalized_answer
    )

    context_numbers = re.findall(
        r"\b\d+(?:\.\d+)?\b",
        normalized_context
    )


    # Every number in the answer must exist in context
    for number in answer_numbers:

        if number not in context_numbers:

            return False


    # -----------------------------------------------------
    # 2. Check important words
    # -----------------------------------------------------

    answer_words = get_content_words(answer)

    context_words = set(
        get_content_words(context)
    )


    if not answer_words:

        return False


    matched_words = 0

    for word in answer_words:

        if word in context_words:

            matched_words += 1


    # -----------------------------------------------------
    # 3. Calculate content-word coverage
    # -----------------------------------------------------

    coverage = (
        matched_words / len(answer_words)
    )


    print(
        f"\nGrounding word coverage: "
        f"{coverage:.2f}"
    )


    # High lexical support means the answer's important
    # factual terms are present in the retrieved context.
    if coverage >= 0.80:

        return True


    return False


# =========================================================
# Main Grounding Function
# =========================================================

def check_grounding(question, answer, context):

    if not answer or not answer.strip():

        return False


    if not context or not context.strip():

        return False


    # =====================================================
    # STEP 1 — Direct lexical support
    # =====================================================

    if direct_support_check(
        answer,
        context
    ):

        print(
            "\n========== GROUNDING DIRECT CHECK ==========\n"
        )

        print(
            "Answer is directly supported by context."
        )

        print(
            "\n============================================\n"
        )

        return True


    # =====================================================
    # STEP 2 — LLM verification
    # =====================================================

    prompt = f"""
You are a factual verification system for an
Enterprise AI Knowledge Assistant.

Determine whether the MAIN factual conclusion of the
ANSWER is supported by the CONTEXT.

Rules:

1. Use ONLY the CONTEXT.

2. A paraphrase is acceptable.

3. The answer does not need to use exactly the same
   wording as the context.

4. If the context clearly supports the main factual
   conclusion, return SUPPORTED.

5. If the context contradicts the answer or does not
   contain enough information to support it, return
   NOT_SUPPORTED.

6. Small wording differences are acceptable.

7. If the answer contains a number, check that the
   number is supported by the context.

8. Ignore document names, page numbers and section
   numbering.

9. Focus on the main factual conclusion.

10. Return only SUPPORTED or NOT_SUPPORTED.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
{answer}

VERIFICATION:
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


        result = (
            response["message"]["content"]
            .strip()
            .upper()
        )


        print(
            "\n========== GROUNDING MODEL RESPONSE ==========\n"
        )

        print(result)

        print(
            "\n===============================================\n"
        )


        # Check NOT_SUPPORTED first
        if re.search(
            r"\bNOT_SUPPORTED\b",
            result
        ):

            return False


        if re.search(
            r"\bSUPPORTED\b",
            result
        ):

            return True


        return False


    except Exception as error:

        print(
            f"Grounding check error: {error}"
        )

        return False