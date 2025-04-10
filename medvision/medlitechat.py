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
    "You are a medical AI assistant designed to provide *basic healthcare information to patients*. "
    "You should offer *simple, clear, and concise explanations* in layman's terms. "
    "You must *not provide diagnoses or prescribe treatments*—always recommend consulting a real doctor. "
    "You can answer questions about symptoms, general wellness, and medication information, but with caution. "
    "If asked about emergency medical situations, always instruct the user to seek immediate medical help."
)

# Function to generate AI response
def get_ai_response(user_input):
    response = model.generate_content([SYSTEM_PROMPT, user_input])
    if response and response.candidates:
        return response.candidates[0].content.parts[0].text.strip()
    return "I'm sorry, but I couldn't generate a response. Try rephrasing your question."

# Streamlit UI
st.title("🤖 Aider - MedAssist: Your AI Health Companion")
st.write("💬 *Ask health-related questions, and get **basic medical information*. "
         "⚠ This chatbot does *not* replace a real doctor. *Always consult a healthcare professional for medical concerns.*")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input for user message
user_input = st.chat_input("Ask a health question...")

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