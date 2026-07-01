import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def _get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_key_here":
        return None
    return OpenAI(api_key=api_key)


def explain_failure(context_text, model=None):
    """Send failure context to OpenAI and return a plain-English explanation."""
    client = _get_client()
    if client is None:
        return (
            "LLM explainer skipped: set OPENAI_API_KEY in .env to enable "
            "automatic failure explanations."
        )

    model = model or DEFAULT_MODEL
    prompt = (
        "You are a senior SDET reviewing an automated test failure.\n"
        "Explain in plain English:\n"
        "1. What likely broke\n"
        "2. Why it failed\n"
        "3. One concrete fix the engineer should try\n\n"
        f"Failure context:\n{context_text}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()
