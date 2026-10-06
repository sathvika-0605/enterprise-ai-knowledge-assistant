from evaluation_dataset import evaluation_questions

from retriever import retrieve_documents
from reranker import rerank_documents

from answer_generator import build_context
from llm import generate_answer
from grounding_checker import check_grounding


# =========================================================
# Evaluation Counters
# =========================================================

total_questions = len(evaluation_questions)

retrieval_correct = 0
answer_correct = 0
grounding_correct = 0


# =========================================================
# Answer Evaluation
# =========================================================

def check_answer(expected_answer, generated_answer):

    expected = expected_answer.lower().strip()
    generated = generated_answer.lower().strip()


    # -----------------------------------------------------
    # Alternative acceptable answers
    # -----------------------------------------------------

    answer_rules = {

        "6 days": [
            "6 days",
            "six days",
            "six (6) days",
            "six [6] days"
        ],

        "10 working days": [
            "10 working days",
            "ten working days"
        ],

        "5 days": [
            "5 days",
            "five days",
            "five (5) days"
        ],

        "182 days": [
            "182 days",
            "182-day",
            "182 day"
        ],

        "when sick leave is taken for more than 1 week": [
            "beyond 1 week",
            "more than 1 week",
            "more than one week",
            "beyond one week"
        ],

        "no, there is no standard wfh allowance.": [
            "no wfh allowance",
            "no standard wfh allowance",
            "wfh is not allowed",
            "not allowed as a standard practice"
        ],

        # -------------------------------------------------
        # Q7 FIX
        # -------------------------------------------------
        "up to 1 day": [
            "up to 1 day",
            "up to one day",
            "1 day",
            "1 day of wfh",
            "one day",
            "one day of wfh"
        ],

        "up to 5 days per calendar year": [
            "up to 5 days per calendar year",
            "5 days of wfh per calendar year",
            "up to five days per calendar year"
        ],

        "a medical report certified by a licensed healthcare professional": [
            "medical report certified by a licensed healthcare professional",
            "medical report",
            "licensed healthcare professional"
        ],

        "they may be permitted to work from home, subject to operational requirements and manager approval.": [
            "may be permitted to work from home",
            "permitted to work from home",
            "subject to operational requirements and manager approval"
        ],

        "29": [
            "29 central labour acts",
            "29 central labour acts were consolidated"
        ],

        "1,228 sections were streamlined into 480 sections": [
            "1,228 sections",
            "1228 sections",
            "480 sections",
            "streamlined into 480"
        ],

        "8 registers": [
            "8 registers",
            "84 to 8",
            "just 8"
        ],

        # -------------------------------------------------
        # Q14 FIX
        # -------------------------------------------------
        "20 or more employees": [
            "20 or more employees",
            "20 or more",
            "20+ employees",
            "20 employees"
        ],

        "26 weeks": [
            "26 weeks",
            "26-week"
        ]
    }


    # -----------------------------------------------------
    # Check acceptable answers
    # -----------------------------------------------------

    if expected in answer_rules:

        for phrase in answer_rules[expected]:

            if phrase in generated:
                return True


    # -----------------------------------------------------
    # Direct match
    # -----------------------------------------------------

    if expected in generated:
        return True


    return False


# =========================================================
# Run Evaluation
# =========================================================

for index, item in enumerate(
    evaluation_questions,
    start=1
):

    question = item["question"]

    expected_answer = item["expected_answer"]

    expected_source = item["expected_source"]


    print("\n" + "=" * 70)

    print(
        f"QUESTION {index}/{total_questions}"
    )

    print(
        f"Question: {question}"
    )


    # =====================================================
    # 1. HYBRID RETRIEVAL
    # =====================================================

    retrieved_documents = retrieve_documents(
        question,
        top_k=10
    )


    # =====================================================
    # 2. CROSS-ENCODER RE-RANKING
    # =====================================================

    reranked_documents = rerank_documents(
        question,
        retrieved_documents,
        top_k=5
    )


    # =====================================================
    # 3. RETRIEVAL EVALUATION
    # =====================================================

    retrieved_sources = [
        document["source"]
        for document in reranked_documents
    ]


    if expected_source in retrieved_sources:

        retrieval_correct += 1

        retrieval_status = "PASS"

    else:

        retrieval_status = "FAIL"


    print(
        f"Expected Source: {expected_source}"
    )

    print(
        f"Retrieved Sources: {retrieved_sources}"
    )

    print(
        f"Retrieval: {retrieval_status}"
    )


    # =====================================================
    # 4. BUILD CONTEXT
    # =====================================================

    context = build_context(
        reranked_documents
    )


    # =====================================================
    # 5. GENERATE ANSWER
    # =====================================================

    try:

        generated_answer = generate_answer(
            question,
            context
        )

    except Exception as error:

        print(
            f"Answer generation error: {error}"
        )

        generated_answer = ""


    # =====================================================
    # 6. ANSWER EVALUATION
    # =====================================================

    answer_status = check_answer(
        expected_answer,
        generated_answer
    )


    if answer_status:

        answer_correct += 1

        answer_result = "PASS"

    else:

        answer_result = "FAIL"


    print(
        f"Expected Answer: {expected_answer}"
    )

    print(
        f"Generated Answer: {generated_answer}"
    )

    print(
        f"Answer: {answer_result}"
    )


    # =====================================================
    # 7. GROUNDING EVALUATION
    # =====================================================

    try:

        grounded = check_grounding(
            question,
            generated_answer,
            context
        )

    except Exception as error:

        print(
            f"Grounding evaluation error: {error}"
        )

        grounded = False


    if grounded:

        grounding_correct += 1

        grounding_result = "PASS"

    else:

        grounding_result = "FAIL"


    print(
        f"Grounding: {grounding_result}"
    )


# =========================================================
# FINAL RESULTS
# =========================================================

retrieval_accuracy = (
    retrieval_correct / total_questions
) * 100


answer_accuracy = (
    answer_correct / total_questions
) * 100


grounding_accuracy = (
    grounding_correct / total_questions
) * 100


# =========================================================
# Evaluation Summary
# =========================================================

print("\n" + "=" * 70)

print(
    "\nEVALUATION SUMMARY"
)

print("=" * 70)

print(
    f"Total Questions: {total_questions}"
)

print(
    f"Retrieval Correct: "
    f"{retrieval_correct}/{total_questions}"
)

print(
    f"Retrieval Accuracy: "
    f"{retrieval_accuracy:.2f}%"
)

print(
    f"Answer Correct: "
    f"{answer_correct}/{total_questions}"
)

print(
    f"Answer Accuracy: "
    f"{answer_accuracy:.2f}%"
)

print(
    f"Grounding Correct: "
    f"{grounding_correct}/{total_questions}"
)

print(
    f"Grounding Accuracy: "
    f"{grounding_accuracy:.2f}%"
)

print("=" * 70)