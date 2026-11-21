
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = """
You are a friendly learning assistant.

Your responsibilities:
1. Answer questions clearly.
2. Explain technical concepts simply.
3. Give examples whenever useful.
4. Remember information from earlier messages.
5. Be polite and supportive.
"""

def get_response(messages):

    contents = []

    for message in messages:
        role = "user" if message["role"] == "user" else "model"

        contents.append(
            types.Content(
                role=role,
                parts=[
                    types.Part.from_text(
                        text=message["content"]
                    )
                ]
            )
        )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )

    if not response.text:
        raise RuntimeError("The AI returned an empty response.")

    return response.text
