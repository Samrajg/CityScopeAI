# 📄 app.py — CityScope AI Chatbot (Clean, Voice-Free)
pip install matplotlib

import streamlit as st
import pandas as pd
import joblib
import random
import base64
import matplotlib.pyplot as plt
import io
import os

# === Page Setup ===
st.set_page_config(page_title="CityScope AI", layout="centered")
st.title("🏙️ CityScope AI Chatbot")

# === Daily Fact Pop-up (Feature 19)
daily_facts = [
    "Madurai is called the Athens of the East.",
    "Chennai has the oldest municipal corporation in India.",
    "Tirunelveli is famous for Halwa and windmills.",
    "Kodaikanal is one of the coolest hill stations in Tamil Nadu.",
    "Kanyakumari is the only place where you can see sunrise and sunset over the ocean."
]
st.info("📌 Fact of the Day: " + random.choice(daily_facts))

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

# === English Tips (fixed)
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

# === Sidebar Buttons and Extras
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🧹 Clear Chat"):
        st.session_state.history = []
        st.rerun()
with col2:
    if st.button("🔁 Refresh Tips"):
        st.rerun()

# === Dark Mode Toggle (Feature 11)
dark_mode = st.sidebar.checkbox("🌙 Enable Dark Mode")
if dark_mode:
    st.markdown("<style>body { background-color: #111; color: #eee; }</style>", unsafe_allow_html=True)

# === Recent FAQs Panel (Feature 6)
with st.sidebar.expander("📊 Frequently Asked"):
    for tip in english_tips[:5]:
        st.markdown(f"- {tip}")

# === District Filter (Feature 4)
districts = sorted(set([q.split()[4] for q in questions if "district" in q.lower()]))
selected_district = st.selectbox("📍 Filter by District (optional)", ["All"] + districts)
if selected_district != "All":
    filtered_indexes = [i for i, q in enumerate(questions) if selected_district.lower() in q.lower()]
else:
    filtered_indexes = list(range(len(questions)))

# === Tips Section
with st.expander("💡 Need help? Try these:", expanded=True):
    for tip in english_tips:
        st.markdown(f"- {tip}")

# === Chat History Display
st.markdown("## 🧠 Chat History")
chat_container = st.container()
with chat_container:
    for q, a in st.session_state.history:
        st.markdown(f"""
        <div style='padding:10px; margin-bottom:10px; background-color:#f1f3f6; border-radius:10px'>
            <b>🧑‍💼 You:</b><br>{q}
        </div>
        <div style='padding:10px; margin-bottom:20px; background-color:#d9fdd3; border-radius:10px'>
            <b>🤖 CityScope AI:</b><br>{a}
        </div>
        """, unsafe_allow_html=True)

# === Chat Input
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input("💬 Ask about Tamil Nadu’s districts:", placeholder="Type your question here...")
    submitted = st.form_submit_button("Send")

# === Run Prediction
if submitted and user_query:
    try:
        query_vec = vectorizer.transform([user_query])
        dist, index = model.kneighbors(query_vec, n_neighbors=len(questions))
        filtered_match = [i for i in index[0] if i in filtered_indexes][0]
        matched_index = filtered_match
        answer = answers[matched_index]

        # === Smart Confidence Feedback (Feature 2)
        if dist[0][0] > 1.0:
            st.warning("🤔 Not fully confident in this answer. Try rephrasing?")

        st.session_state.history.append((user_query, answer))

        # === Map/Image Preview (Feature 3)
        district_keywords = ["chennai", "madurai", "coimbatore", "salem", "namakkal", "tirunelveli", "kanyakumari"]
        for d in district_keywords:
            if d in user_query.lower():
                map_path = f"maps/{d}.png"  # Place images in /maps
                if os.path.exists(map_path):
                    st.image(map_path, caption=f"{d.title()} District Map", use_column_width=True)
                break

        # === Follow-Up Suggestions (Feature 5)
        st.markdown("💬 **You can also ask:**")
        for tip in random.sample(english_tips, 3):
            st.markdown(f"- {tip}")

        st.rerun()
    except Exception as e:
        st.error("⚠️ Failed to process your question.")

# === Data Comparison Mode (Feature 7)
with st.expander("📊 Compare Two Districts"):
    d1 = st.selectbox("District 1", districts, key="d1")
    d2 = st.selectbox("District 2", districts, key="d2")
    if st.button("Compare"):
        q1 = f"What is the population of {d1} district?"
        q2 = f"What is the population of {d2} district?"
        i1 = questions.index(q1) if q1 in questions else -1
        i2 = questions.index(q2) if q2 in questions else -1
        if i1 != -1 and i2 != -1:
            st.success(f"{d1}: {answers[i1]}\n\n{d2}: {answers[i2]}")
        else:
            st.warning("🙁 Comparison data not found.")

# === AI Summary Mode (Feature 15)
with st.expander("🧠 AI Summary"):
    if st.button("Summarize This Chat"):
        combined = " ".join([a for _, a in st.session_state.history])
        st.markdown("📄 **Summary:**")
        st.write(combined[:500] + "..." if len(combined) > 500 else combined)

# === District Ranking View (Feature 16)
with st.expander("🏆 District Rankings"):
    st.markdown("📈 Top 5 Districts by Literacy (sample)")
    ranking_data = {
        "District": ["Chennai", "Kanyakumari", "Coimbatore", "Tiruchirappalli", "Erode"],
        "Literacy Rate": [91.1, 90.2, 89.3, 88.9, 88.1]
    }
    df_rank = pd.DataFrame(ranking_data)
    st.table(df_rank)

# === Data Trend Charts (Feature 20)
with st.expander("📉 Population Trend Demo"):
    years = [2011, 2015, 2021]
    population = [7.1, 7.5, 8.2]
    fig, ax = plt.subplots()
    ax.plot(years, population, marker='o')
    ax.set_title("Chennai Population Growth")
    ax.set_xlabel("Year")
    ax.set_ylabel("Millions")
    st.pyplot(fig)
