import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load API key from .env

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("Please set your GOOGLE_API_KEY in a .env file!")
    st.stop()

# Configure Gemini AI
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Hardcoded default chat model

MODEL_NAME = "gemini-2.5-flash"  
model = gen_ai.GenerativeModel(MODEL_NAME)

# Streamlit page setup

st.set_page_config(
    page_title="Gemini-Chatbot",
    page_icon=":alien:",
    layout="centered"
)

#  Initialize chat session

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display chat history

def translate_role_for_streamlit(user_role):
    """Map Gemini roles to Streamlit roles."""
    return "assistant" if user_role == "model" else user_role

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# -----------------------------
# 6️⃣ User input and model response
# -----------------------------
user_prompt = st.chat_input("Ask ✨Gemini...")
if user_prompt:
    # Show user's message
    st.chat_message("user").markdown(user_prompt)

    # Send message to Gemini-Pro
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Show model's response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
