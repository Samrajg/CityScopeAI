# 📄 app.py — CityScope AI (No location, No dataset, ChatGPT-style UI)

import streamlit as st
import random

# === Page Setup ===
st.set_page_config(page_title="CityScope AI", layout="centered")
st.title("🏙️ CityScope AI Chatbot")

# === Template Answer Logic
def generate_answer(query):
    query_lower = query.lower()
    if "population" in query_lower:
        return "Population data varies by district. You can refer to the Tamil Nadu Census portal for up-to-date info."
    elif "villages" in query_lower:
        return "Tamil Nadu has thousands of villages, each rich in culture and heritage. Specify a district for more."
    elif "education" in query_lower:
        return "Tamil Nadu is known for high literacy and numerous institutions. Major cities have top colleges and schools."
    elif "health" in query_lower:
        return "Each district has government hospitals, PHCs, and health centers. The state also runs Amma clinics in cities."
    elif "industries" in query_lower:
        return "Industries vary by district: Coimbatore for textiles, Hosur for electronics, and Chennai for IT."
    elif "weather" in query_lower:
        return "Tamil Nadu has a tropical climate with hot summers and monsoon rains. Specific data depends on the district."
    else:
        return "I can help you with Tamil Nadu's districts. Ask about population, healthcare, education, industries, etc."

# === Question Tips
tips = [
    "What is the population of Namakkal district?",
    "Tell me about healthcare in Madurai.",
    "What industries are famous in Thoothukudi?",
    "How many villages are in Tirunelveli?",
    "Are there good schools in Coimbatore?",
    "What's the weather like in Kanyakumari?",
    "Tell me something about education in Salem."
]
random.shuffle(tips)

# === Session State
if "history" not in st.session_state:
    st.session_state.history = []

# === Buttons
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []
        st.rerun()
with col2:
    if st.button("🔁 Refresh Tips"):
        st.rerun()

# === Tips Display
with st.expander("💡 Question Tips"):
    for tip in tips:
        st.markdown(f"- {tip}")

# === Chat History
st.markdown("## 🧠 Chat History")
chat_container = st.container()
with chat_container:
    for i, (q, a) in enumerate(st.session_state.history):
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
    user_query = st.text_input("💬 Ask about Tamil Nadu’s districts:", placeholder="Type your question here...")
    submitted = st.form_submit_button("Send")

# === Answering Logic
if submitted and user_query:
    answer = generate_answer(user_query)
    st.session_state.history.append((user_query, answer))
    st.rerun()
