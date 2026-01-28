import streamlit as st
from textblob import TextBlob
from openai import OpenAI
import os

st.set_page_config(page_title="AI Emotion Chatbot", page_icon="🤖")

# ---- API KEY (works local + cloud) ----
api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

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

# ---- AI RESPONSE ----
def chat_with_ai(chat_history):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_history
    )
    return response.choices[0].message.content

# ---- UI ----
st.title("🤖 AI Emotion Chatbot")
st.write("Chat with AI and detect human emotion")

# ---- DISPLAY CHAT HISTORY ----
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# ---- USER INPUT ----
user_input = st.chat_input("Type your message...")

if user_input:
    emotion = detect_emotion(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Show user message instantly
    st.chat_message("user").markdown(user_input)

    # Prepare messages for OpenAI
    openai_messages = [
        {"role": "system", "content": "You are a friendly AI assistant."}
    ] + st.session_state.messages

    # Get AI reply
    ai_reply = chat_with_ai(openai_messages)

    # Save AI reply with emotion
    ai_message = f"🧠 Emotion detected: **{emotion}**\n\n🤖 {ai_reply}"

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_message
    })

    # Show AI reply
    st.chat_message("assistant").markdown(ai_message)
