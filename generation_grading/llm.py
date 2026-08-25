import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemini-3.5-flash-lite"

client = genai.Client(api_key=os.getenv("gemini_api_key"))

if not client:
    print("Error: API Key not found!")
else:
    print("API Key loaded successfully.")

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