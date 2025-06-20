# 📄 app.py — CityScope AI (Clean UI, No APIs, No dataset)

import streamlit as st
import random

# === Page Setup ===
st.set_page_config(page_title="CityScope AI", layout="centered")
st.title("🏙️ CityScope AI Chatbot")

# === Response Engine ===
def generate_answer(query):
    query_lower = query.lower()
    if "population" in query_lower:
        return "Tamil Nadu's population varies by district. You can ask about a specific district like Chennai or Madurai."
    elif "villages" in query_lower:
        return "Districts like Namakkal, Salem, and Tirunelveli have hundreds of villages with rich culture and agriculture."
    elif "education" in query_lower:
        return "Tamil Nadu offers excellent education with government schools, private institutions, and famous colleges."
    elif "health" in query_lower:
        return "The state provides healthcare via PHCs, district hospitals, and special schemes like Amma clinics."
    elif "industries" in query_lower:
        return "Coimbatore is known for textiles, Chennai for IT & automotive, and Salem for steel industries."
    elif "weather" in query_lower:
        return "Tamil Nadu has a tropical climate. Summers are hot, monsoons are moderate, and winters are mild."
    else:
        return "Please ask about population, healthcare, education, industries, villages, or weather in any Tamil Nadu district."

# === Question Tips
tips = [
    "What is the population of Chennai?",
    "Tell me about healthcare in Madurai.",
    "What industries are popular in Coimbatore?",
    "How many villages are in Salem?",
    "Are there good colleges in Tirunelveli?",
    "What's the weather like in Kanyakumari?",
    "Tell me something about education in Erode."
]
random.shuffle(tips)

# === Session State
if "history" not in st.session_state:
    st.session_state.history = []

# === Header Buttons
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []
        st.rerun()
with col2:
    if st.button("🔁 Refresh Tips"):
        st.rerun()

# === Tips UI
with st.expander("💡 Try asking these questions"):
    for tip in tips:
        st.markdown(f"- {tip}")

# === Chat History
st.markdown("## 🧠 Chat History")
chat_container = st.container()
with chat_container:
    for q, a in st.session_state.history:
        st.markdown(f"""
        <div style='padding:10px; margin-bottom:10px; background-color:#f1f3f6; border-radius:10px; color:#000000;'>
            <b>🧑‍💼 You:</b><br>{q}
        </div>
        <div style='padding:10px; margin-bottom:20px; background-color:#d9fdd3; border-radius:10px; color:#000000;'>
            <b>🤖 CityScope AI:</b><br>{a}
        </div>
        """, unsafe_allow_html=True)

# === Chat Input
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("💬 Ask your question about Tamil Nadu districts:", placeholder="Type here...")
    submitted = st.form_submit_button("Send")

# === Chat Response
if submitted and user_query:
    answer = generate_answer(user_query)
    st.session_state.history.append((user_query, answer))
    st.rerun()
