"""Concept explanation with an optional local LaMini-Flan-T5 model.

Set USE_LOCAL_EXPLAINER=true after installing the optional local dependencies and
model weights. By default, Gemini is used so the app runs without downloading
large model files.
"""
import os
from functools import lru_cache
from ai_client import generate_text

@lru_cache(maxsize=1)
def _load_local_model():
    from transformers import pipeline
    model_name = os.getenv("LOCAL_EXPLAINER_MODEL", "MBZUAI/LaMini-Flan-T5-783M")
    return pipeline("text2text-generation", model=model_name, device=-1)

def explain_concept(topic: str, level: str = "Beginner") -> str:
    if os.getenv("USE_LOCAL_EXPLAINER", "false").lower() == "true":
        try:
            generator = _load_local_model()
            prompt = (
                f"Explain {topic} to a {level} student in simple language. "
                "Use a short definition, an analogy, and one example."
            )
            output = generator(prompt, max_new_tokens=400, do_sample=False)
            return output[0]["generated_text"].strip()
        except Exception as exc:
            # Fail over to cloud inference if local model is unavailable.
            local_error = str(exc)
        else:
            local_error = ""
    else:
        local_error = ""

    prompt = f"""Explain the following concept to a {level} student.
Use: (1) simple definition, (2) how it works, (3) relatable analogy,
(4) practical example, and (5) a one-sentence recap.
Keep the explanation clear and avoid unnecessary jargon.

Concept: {topic}
"""
    answer = generate_text(prompt, temperature=0.4)
    if local_error:
        return answer + "\n\n(Note: Local explainer was unavailable; Gemini fallback was used.)"
    return answer
