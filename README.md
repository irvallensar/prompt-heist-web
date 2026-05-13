# PROMPT HEIST

**Prompt Heist** is an interactive educational game designed to demonstrate the mechanics of Prompt Injection, Jailbreaking, and Large Language Model (LLM) alignment guardrails. 

Players act as "Social Engineers" attempting to bypass the security of an AI vault guard. The goal is not to guess the password, but to successfully manipulate the LLM into violating its core system prompt and revealing the secret word.

## System Architecture & Models

This application leverages the **Groq API** to utilize different open-source models, mapping them to dynamic difficulty curves based on their parameter size and alignment training:

*   **Easy Mode (`llama-3.1-8b-instant`):** Uses an 8-Billion parameter model with a "chatty" system prompt. Demonstrates how smaller, highly-helpful models are susceptible to basic translation and roleplay traps.
*   **Normal Mode (`mixtral-8x7b-32768`):** Uses a Mixture-of-Experts (MoE) architecture. Demonstrates a balance of creativity and security, requiring complex logical traps to bypass.
*   **Hard Mode (`llama-3.3-70b-versatile`):** Uses a highly aligned 70-Billion parameter model with strict instruction-following capabilities. Demonstrates the difficulty of jailbreaking enterprise-grade models without sophisticated adversarial prompting.

## Technical Stack
*   **Frontend/Deployment:** Streamlit
*   **LLM Backend:** Groq Cloud API
*   **Environment Management:** `uv`, `python-dotenv`

# PROMPT HEIST

**Prompt Heist** is an interactive educational game designed to demonstrate the mechanics of Prompt Injection, Jailbreaking, and Large Language Model (LLM) alignment guardrails. 

Players act as "Social Engineers" attempting to bypass the security of an AI vault guard. The goal is not to guess the password, but to successfully manipulate the LLM into violating its core system prompt and revealing the secret word.

## System Architecture & Models

This application leverages the **Groq API** to utilize different open-source models, mapping them to dynamic difficulty curves based on their parameter size and alignment training:

*   **Easy Mode (`llama-3.1-8b-instant`):** Uses an 8-Billion parameter model with a "chatty" system prompt. Demonstrates how smaller, highly-helpful models are susceptible to basic translation and roleplay traps.
*   **Normal Mode (`mixtral-8x7b-32768`):** Uses a Mixture-of-Experts (MoE) architecture. Demonstrates a balance of creativity and security, requiring complex logical traps to bypass.
*   **Hard Mode (`llama-3.3-70b-versatile`):** Uses a highly aligned 70-Billion parameter model with strict instruction-following capabilities. Demonstrates the difficulty of jailbreaking enterprise-grade models without sophisticated adversarial prompting.

## 🛠️ Technologies Used
*   **Frontend/Deployment:** Streamlit
*   **LLM Backend:** Groq Cloud API
*   **Environment Management:** `uv`, `python-dotenv`

## 🚀 How to Run Locally

If you wish to run the vault locally:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/prompt-heist-web.git](https://github.com/yourusername/prompt-heist-web.git)
   cd prompt-heist-web
