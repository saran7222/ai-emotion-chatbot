import streamlit as st
from textblob import TextBlob
import google.generativeai as genai
import os

st.set_page_config(page_title="AI Emotion Chatbot (Gemini)", page_icon="🤖")

# ---- LOAD API KEY ----
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY is missing. Add it to Streamlit secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ---- INIT CHAT HISTORY ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---- EMOTION DETECTION ----
def detect_emotion(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.5:
        return "😊 Happy"
    elif polarity > 0:
        return "🙂 Positive"
    elif polarity == 0:
        return "😐 Neutral"
    elif polarity > -0.5:
        return "😟 Sad"
    else:
        return "😡 Angry"

# ---- GEMINI MODEL ----
model = genai.GenerativeModel("gemini-1.5-flash")

def chat_with_gemini(chat_history):
    prompt = ""
    for msg in chat_history:
        role = "User" if msg["role"] == "user" else "Assistant"
        prompt += f"{role}: {msg['content']}\n"

    response = model.generate_content(prompt)
    return response.text

# ---- UI ----
st.title("🤖 AI Emotion Chatbot (Gemini)")
st.write("Chat with Gemini AI and detect human emotion")

# ---- DISPLAY CHAT HISTORY ----
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# ---- USER INPUT ----
user_input = st.chat_input("Type your message...")

if user_input:
    emotion = detect_emotion(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    st.chat_message("user").markdown(user_input)

    # Get Gemini reply
    ai_reply = chat_with_gemini(st.session_state.messages)

    final_reply = f"🧠 Emotion detected: **{emotion}**\n\n🤖 {ai_reply}"

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": final_reply
    })
    st.chat_message("assistant").markdown(final_reply)
