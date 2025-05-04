import streamlit as st
import google.generativeai as genai
import os

# Set your Google Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")  # Prefer env variable

if not GEMINI_API_KEY:
    st.error("Google Gemini API key not set. Please set GEMINI_API_KEY in your environment.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

DISCLAIMER = """
**Disclaimer:** This chatbot is for informational purposes only and does not provide medical advice. 
Always consult a qualified healthcare professional for diagnosis and treatment. 
In case of emergencies, contact your local emergency services immediately.
"""

st.title("🤖 Medical Consultation Chatbot")
st.write("Describe your symptoms or condition, and I'll provide first aid, treatments, and medication suggestions.")
st.markdown(DISCLAIMER)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to generate response from Gemini
def generate_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"""
You are a professional medical consultation assistant. Given the following user description:

"{user_input}"

Provide:
- First aid steps (if needed)
- General treatment advice
- Over-the-counter medicine suggestions with dosage (if safe)
- Clear disclaimer that the user must consult a licensed medical professional before taking any medication

Avoid:
- Diagnosing the user
- Making assumptions about their condition
- Giving definitive medical advice

Be concise and prioritize user safety.
"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ An error occurred while generating the response: `{e}`"

# User input handling
user_input = st.chat_input("Describe your symptoms or condition...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Generating response..."):
        assistant_reply = generate_response(user_input)

    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)

# Footer
st.markdown("---")
st.markdown(DISCLAIMER)
