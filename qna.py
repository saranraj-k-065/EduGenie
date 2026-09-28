from ai_client import generate_text

def answer_question(question: str, level: str = "Beginner") -> str:
    prompt = f"""You are EduGenie, a careful educational tutor.
Answer the student's question clearly and accurately for a {level} learner.
Use a concise explanation, define unfamiliar terms, and include an example when useful.
If the question is ambiguous, state your assumption. Do not invent facts.

Student question:
{question}
"""
    return generate_text(prompt, temperature=0.3)
