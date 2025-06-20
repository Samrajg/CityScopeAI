# 📄 app.py — CityScope AI (Live location-based, no dataset)

import streamlit as st
import requests
import random

# === Page Setup ===
st.set_page_config(page_title="CityScope AI", layout="centered")
st.title("🏙️ CityScope AI Chatbot")

# === Location Detection via IP
def get_location():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json()
        loc = data.get("loc", "")
        city = data.get("city", "")
        region = data.get("region", "")
        return loc, city, region
    except:
        return None, None, None

location, city, region = get_location()

# === Template Answer Logic
def generate_answer(query, city, region):
    if not city:
        return "Sorry, I couldn't detect your location. Please try again later."
    query_lower = query.lower()
    if "population" in query_lower:
        return f"The population data for {city} is currently being updated. Please check the census portal for {region}."
    elif "villages" in query_lower:
        return f"{city} district in {region} has several villages known for agriculture and cultural heritage."
    elif "education" in query_lower:
        return f"{city} has a range of educational institutions, including government schools and colleges in {region}."
    elif "health" in query_lower:
        return f"{city} is served by public health centers and district hospitals under Tamil Nadu Health Dept."
    elif "industries" in query_lower:
        return f"{city} in {region} is known for textiles, small-scale industries, and local manufacturing units."
    elif "weather" in query_lower:
        return f"{city} generally experiences a tropical climate with moderate rainfall across {region}."
    else:
        return f"I'm here to help with district-level info for {city}, {region}. Please ask about population, health, education, etc."

# === Question Tips
tips = [
    "What is the population of my district?",
    "Tell me about healthcare in my area.",
    "What industries are common here?",
    "Give me info about villages in my district.",
    "What's the weather like here?",
    "Are there good schools in my city?",
    "Tell me something about this region."
]
random.shuffle(tips)

# === Session for chat history
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

# === Show Location
if city and region:
    st.markdown(f"📍 **Detected Location**: `{city}, {region}`")
    st.info(f"💡 You can ask about `{city}` or your current region.")

# === Show Tips
with st.expander("💡 Question Tips"):
    for tip in tips:
        st.markdown(f"- {tip}")

# === Chat Display
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
    user_query = st.text_input("💬 Ask about your district or region:", placeholder="Type your question here...")
    submitted = st.form_submit_button("Send")

# === Answering Logic
if submitted and user_query:
    answer = generate_answer(user_query, city, region)
    st.session_state.history.append((user_query, answer))
    st.rerun()
