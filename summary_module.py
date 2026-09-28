from ai_client import generate_text

def summarize_text(text: str, level: str = "Beginner") -> str:
    prompt = f"""Summarize the educational passage for a {level} learner.
Preserve the main ideas and important facts. Use a short overview followed by
3-6 bullet-point key takeaways. Do not add claims absent from the passage.

PASSAGE:
{text}
"""
    return generate_text(prompt, temperature=0.25)
