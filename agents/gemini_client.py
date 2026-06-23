import os
import time
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# We look for GEMINI_API_KEY in the environment.
# If not present in env, we load it from the root .env file explicitly.
if not os.getenv("GEMINI_API_KEY"):
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    load_dotenv(os.path.join(parent_dir, ".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

logger = logging.getLogger("EduPilotGeminiClient")

def generate_content_robust(contents, system_instruction=None, tools=None):
    """Generate content using available Gemini models with retries.

    Supports fallback models, custom system instruction, automatic tool calling,
    and returns a user-friendly error message if all attempts fail.
    """
    models = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash",
    ]

    # Build GenerateContentConfig args
    config_args = {
        "temperature": 0.7,
    }
    if system_instruction:
        config_args["system_instruction"] = system_instruction
    if tools:
        config_args["tools"] = tools

    config = types.GenerateContentConfig(**config_args)

    for model_name in models:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config,
                )
                if response and hasattr(response, "text") and response.text:
                    return response.text
            except Exception as e:
                logger.warning(
                    f"Attempt {attempt+1} with model {model_name} failed: {str(e)}"
                )
                time.sleep(2)

    return (
        "EduPilot AI is currently experiencing high demand. Please try again in a few moments."
    )

def generate_content(prompt):
    """Backward-compatible wrapper for generate_content_robust.

    Tries each model in order up to 3 attempts before falling back to a
    friendly retry message.
    """
    return generate_content_robust(contents=prompt)
