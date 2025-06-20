# -*- coding: utf-8 -*-
"""app.py — CityScope AI Chatbot with ChatGPT UI and Location Detection"""

import streamlit as st
import pandas as pd
import joblib
import random
import requests

# === Page Setup ===
st.set_page_config(page_title="CityScope AI", layout="centered")
st.title("🏙️ CityScope AI Chatbot")

# === Load model and data ===
try:
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    data = pd.read_excel("cityscopedata.xlsx")
except Exception as e:
    st.error("❌ Failed to load model or data. Please check file paths or re-upload.")
    st.stop()

questions = data['Question'].astype(str).tolist()
answers = data['Answer'].astype(str).tolist()

# === Get Location from IP ===
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

# Call location function
location, city, region = get_location()

# === English Tips (static)
english_tips = [
    "What is the population of Namakkal district?",
    "How many villages are there in Tirunelveli?",
    "Tell me about healthcare facilities in Madurai.",
    "What are the key educational institutions in Salem?",
    "Is Coimbatore more urban or rural?",
    "How many towns are in Kanyakumari?",
    "What industries are famous in Thoothukudi?"
]
random.shuffle(english_tips)

# === Session state for chat history
if "history" not in st.session_state:
    st.session_state.history = []

# === Top Buttons: Clear + Refresh
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
    st.info(f"💡 You can ask about `{city}` or nearby districts.")

# === Tips Section
with st.expander("💡 Need help? Try these:", expanded=True):
    for tip in english_tips:
        st.markdown(f"- {tip}")

# === Chat History Display
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

# === Input Form (Sticky Bottom)
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("💬 Ask about Tamil Nadu’s districts:", placeholder="Type your question here...")
    submitted = st.form_submit_button("Send")

# === Run Model
if submitted and user_query:
    try:
        query_vec = vectorizer.transform([user_query])
        dist, index = model.kneighbors(query_vec, n_neighbors=1)
        matched_index = index[0][0]
        answer = answers[matched_index]
        st.session_state.history.append((user_query, answer))
        st.rerun()
    except Exception as e:
        st.error("⚠️ Failed to process your question.")
