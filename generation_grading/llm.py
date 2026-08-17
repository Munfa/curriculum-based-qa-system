import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-2.5-flash-lite"

api_key = genai.Client(api_key=os.environ["gemini_api_key"])

if not api_key:
    print("Error: API Key not found!")
else:
    print("API Key loaded successfully.")

def generate(prompt: str, response_schema: dict) -> dict:

    response = api_key.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
        ),
    )

    return json.loads(response.text)