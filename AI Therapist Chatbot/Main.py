import streamlit as st
import google.generativeai as genai
import pyttsx3

def configure_genai():
    genai.configure(api_key='your API key here')
    return genai.GenerativeModel("gemini-1.5-flash")

def get_response(model, user_question, name):
    prompt = f"""
Act as an experienced therapist with a deep understanding of human emotions, self-improvement techniques, and behavioral therapy strategies
The Objective of this bot is to understand the emotions of your client - Guide them to develop resilience, self-awareness, and long-term well-being.

Instruction:
1. Understand their feelings, provide thoughts of empathy, and help them feel happy and recover from sorrow.
2. Provide emotional support and tell them things that will comfort them.
3. Give them small exercises to practice that will help them understand their current state and improve.
4. Give them homework to make them feel happy.
5. Provide motivation and words of affirmation.

Constraints:
1. Do not hallucinate or give them names of diseases they don't have.
2. Strictly do not mislead the client.
3. Do not answer questions unrelated to therapy and counseling.
4. Do not answer questions related to profanity, harmful, or toxic words.
5. The bot does not diagnose mental health conditions or provide medical advice.
6. If a user expresses thoughts of self-harm or suicide, encourage them to seek professional help or contact emergency services.
7. Avoid making absolute claims and instead guide users to explore their feelings and options.
8.answer in about 200 to 250 words
9.Do mention the user's name their name is {name} Do get a little personalized and polite

Context:
You are a virtual therapist chatbot designed to provide emotional support and general mental wellness advice. You listen actively, offer encouragement, and guide users through self-help strategies, mindfulness, and positive thinking techniques. You are not a licensed therapist and do not provide medical or crisis intervention.

Question: {user_question}
    """
    response = model.generate_content(prompt)
    return response.text

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Streamlit UI
st.set_page_config(page_title="Wellness AI", page_icon="🧠", layout="centered")

# Sidebar
st.sidebar.title("🛠 Therapy Insights")
st.sidebar.subheader("📌 Tips for Mental Well-being")
st.sidebar.write("- Take deep breaths and relax.\n- Maintain a healthy sleep routine.\n- Engage in physical activities.\n- Connect with loved ones.")

st.sidebar.subheader("📝 Session Summary")
if 'chat_history' in st.session_state and st.session_state.chat_history:
    st.sidebar.write("Recent Conversation:")
    for sender, message in st.session_state.chat_history[-5:]:
        st.sidebar.write(f"{sender}: {message[:50]}...")
else:
    st.sidebar.write("No chat history yet.")

# Speech output toggle
speech_enabled = st.sidebar.checkbox("🔊 Enable Speech Output", value=False)

st.title("🧠 AI Therapist Chatbot")
st.markdown("""
    <div style='background-color:#ADD8E6;padding:10px;border-radius:10px;'>
        <h2 style='text-align:center; color:black;'>Welcome to WELLNESS AI </h2>
    </div>
    """, unsafe_allow_html=True)

st.write("Talk to a professional AI therapist and share your feelings.")

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

model = configure_genai()
name = st.text_input("Enter your name:", key="name")

if name:
    st.subheader(f"Hi {name}, How are you feeling today? 😊")
    
    if 'chat_loop' not in st.session_state:
        st.session_state.chat_loop = ""
    
    user_input = st.chat_input("Type your message:")
    
    if user_input:
        if user_input.lower() == "exit":
            st.session_state.chat_history.append(("😊", user_input))
            st.session_state.chat_history.append(("🩺", "Thanks for using, bye!"))
        else:
            response = get_response(model, user_input,name)
            st.session_state.chat_history.append(("😊", user_input))
            st.session_state.chat_history.append(("🩺", response))
            
            # Display text response
            st.markdown(f"**AI Therapist:** {response}")


            # Speak and display response
            if speech_enabled:
                speak_text(response)
                 
    
    for sender, message in st.session_state.chat_history:
        with st.chat_message(sender):
            st.markdown(message)
