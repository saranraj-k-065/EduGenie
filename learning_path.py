from ai_client import generate_text

def get_learning_recommendations(topic: str, level: str = "Beginner") -> str:
    prompt = f"""Create a personalized learning roadmap for: {topic}
Learner's current level: {level}
Organize it from foundations to advanced topics. Include:
- stages in order, with suggested time estimates
- concepts and hands-on mini-projects for each stage
- practice/revision checkpoints
- resource types or well-known official documentation/books where appropriate
- a final capstone project
Do not fabricate URLs. If unsure of a URL, give the resource title or organization only.
Format with clear Markdown headings and lists.
"""
    return generate_text(prompt, temperature=0.4)
