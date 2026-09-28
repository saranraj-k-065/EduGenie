from ai_client import get_client, GEMINI_MODEL

client = get_client()

print("Testing model:", GEMINI_MODEL)

response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="Explain Python in two sentences."
)

print(response.text)