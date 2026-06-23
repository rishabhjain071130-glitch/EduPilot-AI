import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

def generate_content(prompt):
    """Generate content using available Gemini models with retries.

    Tries each model in order up to 3 attempts before falling back to a
    friendly retry message.
    """

    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
    ]

    for model_name in models:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                # response.text is expected to contain the generated text
                return getattr(response, "text", None) or str(response)
            except Exception:
                time.sleep(3)

    return (
        "⚠️ EduPilot AI is temporarily experiencing high demand.\n\n"
        "Please try again in a few moments."
    )
