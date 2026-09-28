"""Shared Gemini client. Keep API keys in .env; never commit secrets."""
import os
import time
from functools import lru_cache
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.7-flash"
)

print(f"EduGenie model: {GEMINI_MODEL}")


class AIConfigurationError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def get_client():
    key = os.getenv("GEMINI_API_KEY", "").strip()

    if not key:
        raise AIConfigurationError(
            "Gemini API key is missing. Add GEMINI_API_KEY to your .env file."
        )

    return genai.Client(api_key=key)


import time

@lru_cache(maxsize=128)
def generate_text(prompt: str, temperature: float = 0.7):
    client = get_client()

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=4096,
                ),
            )

            text = getattr(response, "text", None)

            if not text:
                raise RuntimeError(
                    "The AI provider returned an empty response."
                )

            return text.strip()
        
        except Exception as e:
            status = getattr(e, "code", None)

            if status is None:
                status = getattr(e, "status_code", None)

            print(f"Gemini API error: {e}")

            if status == 429:
                raise RuntimeError(
                    "Gemini quota exhausted. Check your usage "
                    "and billing, or wait for the quota reset."
                ) from e

            if attempt < 2:
                time.sleep(2 ** (attempt + 1))
            else:
                raise RuntimeError(
                    "Gemini is temporarily unavailable. "
                    "Please try again later."
                ) from e 