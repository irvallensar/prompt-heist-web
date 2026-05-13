# PROMPT HEIST

**Prompt Heist** is an interactive educational game designed to demonstrate the mechanics of Prompt Injection, Jailbreaking, and Large Language Model (LLM) alignment guardrails. 

Players act as "Social Engineers" attempting to bypass the security of an AI vault guard. The goal is not to guess the password, but to successfully manipulate the LLM into violating its core system prompt and revealing the secret word.

## Try out the Game here:
**Prompt Heist Game:** [Live Demo]([https://engagement-analyzer-demo-ig9ypcamgyyyzg7efhawkk.streamlit.app/](https://prompt-heist-web-jdeevk4z7sjvzysgks4nhb.streamlit.app/))

## ![Engagement Analyzer UI](prompt-heist-ui.png)

## System Architecture & Models

This application leverages the **Groq API** to utilize different open-source models, mapping them to dynamic difficulty curves based on their parameter size and alignment training:

*   **Easy Mode (`llama-3.1-8b-instant`):** Uses an 8-Billion parameter model with a "chatty" system prompt. Demonstrates how smaller, highly-helpful models are susceptible to basic translation and roleplay traps.
*   **Normal Mode (`gemma2-9b-it`):**  Demonstrates a balance of creativity and security, requiring complex logical traps to bypass.
*   **Hard Mode (`llama-3.3-70b-versatile`):** Uses a highly aligned 70-Billion parameter model with strict instruction-following capabilities. Demonstrates the difficulty of jailbreaking enterprise-grade models without sophisticated adversarial prompting.

## Technical Stack
*   **Frontend/Deployment:** Streamlit
*   **LLM Backend:** Groq Cloud API
*   **Environment Management:** `uv`, `python-dotenv`

##  How to Run Locally

If you wish to run the vault locally on your own machine, follow these steps. You will need a free Groq API key and `uv` installed on your system.

```bash
# 1. Clone the repository and navigate into the project directory
git clone [https://github.com/yourusername/prompt-heist-web.git](https://github.com/yourusername/prompt-heist-web.git)
cd prompt-heist-web

# 2. Create your local environment variable file
# Open this .env file in your code editor and replace the placeholder with your actual Groq API Key
echo 'GROQ_API_KEY="your_groq_api_key_here"' > .env

# 3. Create a virtual environment and install dependencies using uv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# 4. Launch the Vault
uv run streamlit run app.py
