from app.services.openai_service import generate_questions

topic = "AI in the workplace"
questions = generate_questions(topic)

print("Generated questions:")
for q in questions:
    print("-", q)