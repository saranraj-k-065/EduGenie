
import json
import re
from ai_client import generate_text


def clean_json_block(text: str) -> str:
    """Remove Markdown fences and extract JSON."""
    cleaned = text.strip()
    cleaned = re.sub(
        r"^```(?:json)?\s*", "", cleaned,
        flags=re.IGNORECASE
    )
    cleaned = re.sub(r"\s*```$", "", cleaned)

    start_array = cleaned.find("[")
    end_array = cleaned.rfind("]")
    start_obj = cleaned.find("{")
    end_obj = cleaned.rfind("}")

    if start_array != -1 and end_array > start_array:
        return cleaned[start_array:end_array + 1]

    if start_obj != -1 and end_obj > start_obj:
        return cleaned[start_obj:end_obj + 1]

    return cleaned


def generate_quiz(content: str, level: str = "Beginner") -> list:
    prompt = f"""Create exactly 3 educational multiple-choice
questions based only on the content below for a {level} learner.

Each question must have four options labeled A, B, C, D,
one correct answer, and a short explanation.

Return ONLY valid JSON in this schema:

[
  {{
    "question": "...",
    "options": {{
      "A": "...",
      "B": "...",
      "C": "...",
      "D": "..."
    }},
    "answer": "A",
    "explanation": "..."
  }}
]

The answer must be the option letter.
Do not include Markdown fences.

CONTENT:
{content}
"""

    raw = generate_text(prompt, temperature=0.2)

    try:
        data = json.loads(clean_json_block(raw))

        if isinstance(data, dict):
            data = data.get("questions", [])

        if not isinstance(data, list) or len(data) != 3:
            raise ValueError("Expected exactly three questions.")

        for item in data:
            if not all(
                k in item
                for k in (
                    "question",
                    "options",
                    "answer",
                    "explanation"
                )
            ):
                raise ValueError(
                    "A question is missing required fields."
                )

            if set(item["options"].keys()) != {
                "A", "B", "C", "D"
            }:
                raise ValueError(
                    "Each question must have A, B, C, and D options."
                )

            item["answer"] = str(
                item["answer"]
            ).strip().upper()

            if item["answer"] not in {"A", "B", "C", "D"}:
                raise ValueError(
                    "Answer must be A, B, C, or D."
                )

        return data

    except (json.JSONDecodeError, ValueError, TypeError) as exc:
        raise RuntimeError(
            f"Could not parse quiz JSON: {exc}. Try again."
        ) from exc