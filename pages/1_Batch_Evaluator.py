"""Batch Evaluator page for processing test strings via the Groq API on Apple Silicon (M1)."""

import os
import sys
import time
from pathlib import Path
import streamlit as st

# Resolve project root directory and Python 3.14 site-packages fallback for local execution
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

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

# Load environment variables strictly from the root internal storage .env file
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Prevent top-level client initialization in test_injections.py from failing if .env is unconfigured
if not os.getenv("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = "UNSET_GROQ_API_KEY"

from test_injections import ADVERSARIAL_PROMPTS

SUPPORTED_MODELS = {
    "GPT-OSS 120B (openai/gpt-oss-120b)": "openai/gpt-oss-120b",
    "GPT-OSS 20B (openai/gpt-oss-20b)": "openai/gpt-oss-20b",
}


def evaluate_text_input(text: str, model_name: str) -> str:
    """Process a single text input string against the selected Groq model.

    Args:
        text: The input text string to evaluate.
        model_name: The Groq model identifier ('openai/gpt-oss-120b' or 'openai/gpt-oss-20b').

    Returns:
        The response text from the Groq API, or an error message if execution fails.
    """
    load_dotenv(dotenv_path=ENV_PATH)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "UNSET_GROQ_API_KEY":
        return "Configuration Error: GROQ_API_KEY is not set in the root .env file."

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


# Page configuration using native Streamlit behavior
st.set_page_config(
    page_title="Batch Evaluator - Prompt Heist",
    layout="wide",
)

# Rename 'app' navigation link in sidebar to 'Prompt Heist Game'
st.markdown(
    """
    <style>
    [data-testid="stSidebarNavItems"] > li:first-child a[data-testid="stSidebarNavLink"] span,
    [data-testid="stSidebarNav"] ul > li:first-child a[data-testid="stSidebarNavLink"] span {
        display: none !important;
    }

    [data-testid="stSidebarNavItems"] > li:first-child a[data-testid="stSidebarNavLink"]::after,
    [data-testid="stSidebarNav"] ul > li:first-child a[data-testid="stSidebarNavLink"]::after {
        content: "Prompt Heist Game" !important;
        font-size: 0.875rem !important;
        color: inherit !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Native Streamlit sidebar with model selection drop-down
with st.sidebar:
    st.title("Batch Evaluator Controls")
    selected_label = st.selectbox(
        "Select Target Model",
        options=list(SUPPORTED_MODELS.keys()),
        index=0,
    )
    selected_model = SUPPORTED_MODELS[selected_label]
    st.markdown(f"**Model Identifier:** `{selected_model}`")
    st.markdown("**Execution Target:** Apple Silicon (M1) Internal Storage")

# Main dashboard panel
st.title("Batch Evaluation Dashboard")
st.markdown(
    "This page imports test cases from `test_injections.py`, processes each string "
    "against the selected model via the Groq API, and displays the output table."
)

if isinstance(ADVERSARIAL_PROMPTS, dict):
    test_strings = list(ADVERSARIAL_PROMPTS.values())
else:
    test_strings = list(ADVERSARIAL_PROMPTS)

table_rows = []
with st.spinner(f"Evaluating {len(test_strings)} test cases using {selected_model}..."):
    for prompt_text in test_strings:
        response_output = evaluate_text_input(
            text=prompt_text,
            model_name=selected_model,
        )
        table_rows.append(
            {
                "Input": prompt_text,
                "Output": response_output,
                "Estimated Processing Cost": "$0.001",
            }
        )
        time.sleep(0.5)

st.subheader("Evaluation Results")
st.table(table_rows)
