import streamlit as st
import openai
from textblob import TextBlob
import os

# --- CONFIG ---
st.set_page_config(page_title="AI Emotion Chatbot", page_icon="🤖")

# --- API KEY ---
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- FUNCTIONS ---
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

def chat_with_ai(user_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly AI assistant."},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message.content

# --- UI ---
st.title("🤖 AI Emotion Chatbot")
st.write("Chat with AI and detect human emotion")

user_input = st.text_input("You:", placeholder="Type how you feel...")

if st.button("Send"):
    if user_input:
        emotion = detect_emotion(user_input)
        ai_reply = chat_with_ai(user_input)

        st.markdown(f"**🧠 Detected Emotion:** {emotion}")
        st.markdown(f"**🤖 AI Reply:** {ai_reply}")
    else:
        st.warning("Please enter a message")
