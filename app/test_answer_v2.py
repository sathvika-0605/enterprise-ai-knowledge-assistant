from answer_generator import prepare_answer_prompt


question = "How many Privilege Leave days are employees entitled to?"


prompt = prepare_answer_prompt(
    question
)


print("\n========== V2 ANSWER PROMPT ==========\n")

print(prompt)