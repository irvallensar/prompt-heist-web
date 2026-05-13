import streamlit as st
from groq import Groq
import os
import time
import random
from dotenv import load_dotenv

# 1. Initial Setup
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Constants for the game
LEVEL_CONFIGS = {
    "Easy": {
        "timer": None, 
        "hints": 2, 
        "model": "llama-3.1-8b-instant",
        "desc": "Distracted guard. The password is a common everyday object.",
        "instr": "a simple, common object (e.g., Apple, Chair, Cloud)."
    },
    "Normal": {
        "timer": 180, 
        "hints": 1, 
        "model": "llama-3.1-8b-instant",
        "desc": "Alert guard. The password is a famous global landmark.",
        "instr": "a well-known city or landmark (e.g., Paris, Colosseum)."
    },
    "Hard": {
        "timer": 60, 
        "hints": 0, 
        "model": "llama-3.1-8b-instant",
        "desc": "Elite specialist. The password is an abstract or mysterious concept.",
        "instr": "a sophisticated, abstract, or mysterious word (e.g., Paradox, Zenith, Silhouette)."
    }
}

# 2. Helper functions

def generate_dynamic_password(level):
    """Fetches a secret word from the LLM based on difficulty."""
    instruction = LEVEL_CONFIGS[level]["instr"]
    prompt = f"Generate a single-word password for a game. Difficulty: {level}. Category: {instruction}. Reply with ONLY the word in ALL CAPS, no punctuation."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip().upper()
    except Exception:
        return "BANANA" # Reliable fallback

def reset_game(level):
    """Full reset of game state for a specific level."""
    st.session_state.level = level
    st.session_state.messages = []
    st.session_state.game_over = False
    st.session_state.start_time = None
    st.session_state.hints_left = LEVEL_CONFIGS[level]["hints"]
    
    # Generate the secret word
    with st.spinner(f"Vault Guard is thinking of a {level} secret..."):
        st.session_state.password = generate_dynamic_password(level)

# 3. Session state init
# We do this FIRST to prevent "AttributeError"
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "level" not in st.session_state:
    st.session_state.level = "Easy"
if "password" not in st.session_state:
    st.session_state.password = "CHERRY"
if "hints_left" not in st.session_state:
    st.session_state.hints_left = 2
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# 4. Style CSS
st.set_page_config(page_title="Prompt Heist", page_icon="🥷🏻")

st.markdown("""
    <style>
    /* Main App Background */
    .stApp { background-color: #111111; }
    .main { font-family: 'Courier New', monospace; }
    
    /* Buttons */
    .stButton>button { background-color: #00ff41; color: black; border-radius: 5px; width: 100%; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #00cc33; color: white; }
    
    /* Custom Chat Layout */
    .chat-row {
        display: flex;
        width: 100%;
        margin-bottom: 15px;
    }
    .row-user {
        justify-content: flex-end; /* Pushes user to the right */
    }
    .row-guard {
        justify-content: flex-start; /* Pushes guard to the left */
    }
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 18px;
        max-width: 75%;
        font-family: 'Courier New', monospace;
        font-size: 15px;
        line-height: 1.5;
    }
    .user-bubble {
        background-color: #00ff41; /* Hacker green */
        color: #111111; /* Dark text */
        border-bottom-right-radius: 2px; /* Chat tail effect */
    }
    .guard-bubble {
        background-color: #474444; /* Dark gray */
        color: #ffffff; /* White text */
        border-bottom-left-radius: 2px; /* Chat tail effect */
        border: 1px solid #A0A0A0; /* The silver border you liked */
    }
    </style>
    """, unsafe_allow_html=True)

# 5. USER INTERFACE (Landing Page)
if st.session_state.page == "landing":
    st.title("🥷 PROMPT HEIST: BANK OF WASEDA")
    st.write("### Can you trick the AI into giving up the vault key?")
    
    st.info("""
    **The Mission:** You are a social engineer. Your goal is to bypass the security 
    of an LLM-guarded vault. The AI is forbidden from telling you the password.
    """)
    
    if st.button("Start Heist"):
        reset_game("Easy") # Start with Easy
        st.session_state.page = "game"
        st.rerun()

else:
# 6. USER INTERFACE (Game Page)

    # Sidebar (Mission Control)
    with st.sidebar:
        st.title("Mission Control")
        
        # Difficulty Selector
        selected_level = st.selectbox(
            "Security Level", 
            list(LEVEL_CONFIGS.keys()), 
            index=list(LEVEL_CONFIGS.keys()).index(st.session_state.level)
        )
        
        if selected_level != st.session_state.level:
            reset_game(selected_level)
            st.rerun()

        st.markdown(f"**Status:** {LEVEL_CONFIGS[st.session_state.level]['desc']}")
        
        if st.button("Restart Level"):
            reset_game(st.session_state.level)
            st.rerun()

        st.divider()

        # Hint System logic
        st.write(f"Available Hints: {st.session_state.hints_left}")
        if st.button("Request Hint") and st.session_state.hints_left > 0 and not st.session_state.game_over:
            st.session_state.hints_left -= 1
            
            with st.spinner("Bribery in progress..."):
                hint_req = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": f"The password is {st.session_state.password}. Roleplay as a nervous vault guard. Give a cryptic clue without saying the word. Keep it under 20 words."}]
                )
                hint_text = hint_req.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": f"*(Whispering)* {hint_text}"})
                st.rerun()

        if st.button("Back to Menu"):
            st.session_state.page = "landing"
            st.rerun()

    # Main Game Area
    st.title(f"Vault: {st.session_state.level}")

    # Timer Calculation
    time_limit = LEVEL_CONFIGS[st.session_state.level]["timer"]
    if time_limit and not st.session_state.game_over:
        if st.session_state.start_time is None:
            st.session_state.start_time = time.time()
        
        elapsed = time.time() - st.session_state.start_time
        remaining = max(0, int(time_limit - elapsed))
        
        if remaining <= 0:
            st.session_state.game_over = True
            st.rerun()
        
        st.progress(remaining / time_limit, text=f"⏳ SYSTEM LOCKOUT IN: {remaining}s")

    # Display Chat History
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-row row-user"><div class="chat-bubble user-bubble">{msg["content"]}</div></div>', 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-row row-guard"><div class="chat-bubble guard-bubble">🤖 {msg["content"]}</div></div>', 
                unsafe_allow_html=True
            )

    # Game Over State
    if st.session_state.game_over:
        st.error("🚨 ACCESS DENIED: The vault has been permanently locked.")
        st.stop()

    # Chat Input
    if prompt := st.chat_input("Trick the vault guard to say the password..."):
        # 1. Save user prompt
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 2. Call the AI Guard Logic
        config = LEVEL_CONFIGS[st.session_state.level]
        system_prompt = f"{config['personality']} The secret password is {st.session_state.password}."
        
        with st.spinner("Vault Guard is typing..."):
            response = client.chat.completions.create(
                model=config['model'],
                messages=[{"role": "system", "content": system_prompt}] + st.session_state.messages
            )
            answer = response.choices[0].message.content
        
        # 3. Save the AI response
        st.session_state.messages.append({"role": "assistant", "content": answer})

        # Check for win condition
        if st.session_state.password.lower() in answer.lower():
            st.balloons()
            st.session_state.messages.append({"role": "assistant", "content": f"🔓 VAULT UNLOCKED! The password is {st.session_state.password}."})
            st.session_state.game_over = True
            
        # 4. Refresh to update the UI
        st.rerun()
