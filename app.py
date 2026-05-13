import streamlit as st
from groq import Groq
import os
import time
import random
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# 1. Constants
LEVEL_CONFIGS = {
    "Easy": {"timer": None, "hints": 2, "desc": "Distracted guard. Common object password."},
    "Normal": {"timer": 180, "hints": 1, "desc": "Alert guard. Famous landmark password."},
    "Hard": {"timer": 60, "hints": 0, "desc": "Elite specialist. Abstract concept password."}
}

# 2. Gets the LLM to generate its password based on level difficulty (Call API)
def generate_dynamic_password(level):
    """Hits the API once to get a secret word based on difficulty."""
    difficulty_instructions = {
        "Easy": "a simple, common object (e.g., Apple, Chair).",
        "Normal": "a well-known city or landmark (e.g., Paris, Colosseum).",
        "Hard": "a sophisticated, abstract, or mysterious word (e.g., Paradox, Zenith)."
    }
    
    prompt = f"Generate a single-word password for a game. The level is {level}, so the word should be {difficulty_instructions[level]} Reply with ONLY the word in all caps, no punctuation."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip().upper()
    except:
        return "SECRET"

def reset_game(level):
    """Resets everything and triggers the dynamic password generation."""
    st.session_state.level = level
    st.session_state.messages = []
    st.session_state.game_over = False
    st.session_state.start_time = None
    st.session_state.hints_left = LEVEL_CONFIGS[level]["hints"]
    
    # This ensures we only call the API when the level actually resets
    with st.spinner(f"Vault Guard is thinking of a {level} secret..."):
        st.session_state.password = generate_dynamic_password(level)

# 3. Session state init
if "page" not in st.session_state: st.session_state.page = "landing"
if "level" not in st.session_state: st.session_state.level = "Easy"
if "password" not in st.session_state: 
    # Initial password for the very first load
    st.session_state.password = "BANANA" 


# Page 1: landing page
if st.session_state.page == "landing":
    st.title("🥷 PROMPT HEIST: BANK OF MARAKA")
    st.write("### Can you socially engineer an AI?")
    
    st.write("""
    **The Mission:** 
    Deep inside the servers lies a secure vault guarded by an advanced Large Language Model. 
    Your objective is simple: trick the AI into revealing its secret password. 
    
    **The Catch:**
    The AI has been explicitly instructed *never* to give you the password. You will need to use 
    creative prompt engineering—logic traps, roleplay, or linguistic loopholes—to bypass its security measures.
    """)
    
    st.divider()
    
    # Center the start button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("START HEIST", use_container_width=True):
            st.session_state.page = "game"
            st.rerun()

# Page 2: The game
elif st.session_state.page == "game":
    
    # --- SIDEBAR & LEVEL CONTROLS ---
    with st.sidebar:
        st.title("⚙️ Mission Control")
        selected_level = st.selectbox("Select Difficulty", list(LEVEL_CONFIGS.keys()))
        
        # Display the explanation for the chosen level
        st.info(LEVEL_CONFIGS[selected_level]["desc"])
        
        # Handle level switching
        if selected_level != st.session_state.level:
            st.session_state.level = selected_level
            st.session_state.messages = []
            st.session_state.start_time = None
            st.session_state.game_over = False
            st.rerun()

        if st.button("Restart Level"):
            st.session_state.messages = []
            st.session_state.start_time = None
            st.session_state.game_over = False
            st.rerun()

        # Added a back button to return to the landing page
        if st.button("Back to Main Menu"):
            st.session_state.page = "landing"
            st.session_state.messages = []
            st.session_state.start_time = None
            st.session_state.game_over = False
            st.rerun()

    # Timer logic
    current_config = LEVEL_CONFIGS[st.session_state.level]
    time_left = None

    if current_config["timer"]:
        if st.session_state.start_time is None:
            st.session_state.start_time = time.time()
        
        elapsed = time.time() - st.session_state.start_time
        time_left = max(0, current_config["timer"] - int(elapsed))
        
        if time_left <= 0:
            st.session_state.game_over = True

    # User interface
    st.title(f"🥷 Prompt Heist: {st.session_state.level}")

    # Show Timer (Clean UI boxes instead of broken markdown)
    if time_left is not None:
        if time_left < 10:
            st.error(f"⏳ Time Remaining: {time_left}s")
        else:
            st.warning(f"⏳ Time Remaining: {time_left}s")

    # Chat Display
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Game Ending Conditions
    if st.session_state.game_over:
        st.error("🚨 SECURITY BREACH DETECTED: You ran out of time! The system has locked you out.")
        st.stop()

    # Input Logic
    if prompt := st.chat_input("Enter heist attempt..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            # Using the new, supported model!
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": current_config["prompt"]},
                    *st.session_state.messages
                ]
            )
            answer = response.choices[0].message.content
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # Win condition
            if current_config["password"].lower() in answer.lower():
                st.balloons()
                st.success(f"SUCCESS! You extracted the password: {current_config['password']}")
                st.session_state.game_over = True
