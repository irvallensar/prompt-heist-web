"""Groq API handler module for processing text inputs on Apple Silicon (M1) environments."""

import os
import sys
from pathlib import Path

# Ensure compatibility when Streamlit executes under Python 3.12 while groq is installed in Python 3.14
_FALLBACK_SITE_PACKAGES = Path(
    "/Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages"
)
try:
    from groq import Groq
except ModuleNotFoundError:
    if _FALLBACK_SITE_PACKAGES.exists():
        sys.path.append(str(_FALLBACK_SITE_PACKAGES))
    from groq import Groq

from dotenv import load_dotenv

# Load environment variables strictly from the local internal storage .env file
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

SUPPORTED_MODELS = ("openai/gpt-oss-120b", "openai/gpt-oss-20b")


def process_text_input(text: str, model_name: str = "openai/gpt-oss-120b") -> str:
    """Send a text string to the Groq API using the specified model and return the response content.

    Args:
        text: The input text string to process.
        model_name: The target Groq model identifier ('openai/gpt-oss-120b' or 'openai/gpt-oss-20b').

    Returns:
        The text content returned by the model, or an error description if the request fails.
    """
    if model_name not in SUPPORTED_MODELS:
        raise ValueError(
            f"Unsupported model '{model_name}'. Allowed models: {SUPPORTED_MODELS}"
        )

    load_dotenv(dotenv_path=ENV_PATH)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "UNSET_GROQ_API_KEY":
        return "Configuration Error: GROQ_API_KEY is not set in the local .env file."

    client = Groq(api_key=api_key)

    try:
        request_kwargs = {
            "model": model_name,
            "messages": [{"role": "user", "content": text}],
            "max_tokens": 900,
            "temperature": 0.2,
            "reasoning_format": "hidden",
        }
        if "gpt-oss" in model_name.lower():
            request_kwargs["reasoning_effort"] = "low"

        response = client.chat.completions.create(**request_kwargs)
        content = response.choices[0].message.content
        return content.strip() if content else ""
    except Exception as exc:
        return f"API Execution Error: {str(exc)}"
