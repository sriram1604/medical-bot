import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure the Gemini AI model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# System Prompt to Instruct the AI
SYSTEM_PROMPT = (
    "You are a medical AI chatbot designed to assist doctors only. "
    "You must only answer healthcare-related questions, including diagnosis, treatment options, "
    "medical conditions, drug interactions, and professional medical procedures. "
    "If the question is unrelated to medicine, refuse to answer. "
    "All information you provide is strictly for **doctors and medical professionals only**, "
    "so you may use in-depth terminology and elaborate medical explanations."
)

# Function to generate AI response
def get_ai_response(user_input):
    response = model.generate_content([SYSTEM_PROMPT, user_input])
    if response and response.candidates:
        return response.candidates[0].content.parts[0].text.strip()
    return "I'm sorry, but I couldn't generate a response. Try rephrasing your question."

# Streamlit UI
st.title("🩺 MedVision AI: Doctor’s Medical Assistant")
st.write("💬 This chatbot is designed exclusively for **healthcare professionals**. "
         "Ask detailed medical questions for expert-level insights.")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input for user message
user_input = st.chat_input("Ask a medical question...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    response = get_ai_response(user_input)

    # Display AI response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
