from app.answer_generator import prepare_answer_prompt


question = "How many days of work from home are allowed?"

prompt = prepare_answer_prompt(question)

print("\nGenerated Prompt:\n")
print(prompt)