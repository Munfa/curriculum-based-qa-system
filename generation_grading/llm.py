import os
import json
from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash-lite"

client = genai.Client(
    api_key=os.environ["gemini_api_key"]
)

def generate(prompt: str, response_schema: dict) -> dict:

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
    )

    return json.loads(response.text)