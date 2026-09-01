import json

from backend.config import GEMINI_API_KEY, GEMINI_MODEL

def generate(prompt: str, response_schema: dict) -> dict:
    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not set. "
            "Add it to a .env file before using QA, MCQ, or CQ generation."
        )

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        return json.loads(response.text)
    
    except ImportError as exc:
        raise RuntimeError(
            "The google-genai package is not installed. "
            "Run: python -m pip install -r requirements.txt"
        ) from exc
    except Exception as exc:
        raise RuntimeError(f"LLM call failed: {exc}") from exc
