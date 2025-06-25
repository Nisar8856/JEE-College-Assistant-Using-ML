
import streamlit as st
import numpy as np
import pickle

# Set page configuration
st.set_page_config(page_title="🎯 JEE College Assistant", layout="centered")

# Load your trained model
model = pickle.load(open("model1.pkl", "rb"))

# Inject custom CSS to style the app
st.markdown("""
    <style>
    body {
        background-color: #0f1117;
    }
    .main {
        background-color: #111827;
        padding: 2rem;
        border-radius: 10px;
        color: white;
    }
    .stSelectbox > div, .stNumberInput > div {
        background-color: #1f2937 !important;
        color: white !important;
    }
    .stButton > button {
        background-color: #2563eb !important;
        color: white !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.markdown("<h1 style='text-align: center; color: #facc15;'>🎓 JEE College Assistant </h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Predict your best-fit colleges based on rank and preferences</p>", unsafe_allow_html=True)

# Sidebar with uploaded logo and inputs
st.sidebar.image("logo1.png", use_container_width=True)
st.sidebar.title("📌 Input Your Details")

# User Inputs
category = st.sidebar.selectbox("Category", ["General", "OBC", "SC", "ST", "EWS"])
quota = st.sidebar.selectbox("Quota", ["AI", "HS", "OS"])
pool = st.sidebar.selectbox("Gender Pool", ["Gender-Neutral", "Female-only"])
institute_type = st.sidebar.selectbox("Institute Type", ["NIT", "IIT"])
round_no = st.sidebar.selectbox("Round Number", list(range(1, 7)))
opening_rank = st.sidebar.number_input("Opening Rank", min_value=1, max_value=500000, value=2000)
closing_rank = st.sidebar.number_input("Closing Rank", min_value=1, max_value=500000, value=2841)

# Encode inputs for the ML model
encoded_input = [
    0 if category == "General" else 1 if category == "OBC" else 2 if category == "SC" else 3 if category == "ST" else 4,
    0 if quota == "AI" else 1 if quota == "HS" else 2,
    0 if pool == "Gender-Neutral" else 1,
    1 if institute_type == "NIT" else 0,
    round_no,
    opening_rank,
    closing_rank
]

# Prediction section
st.markdown("<hr style='border: 1px solid #374151;'>", unsafe_allow_html=True)

if st.button("🎯 Find My Top College Match Now!"):
    predictions = model.predict([encoded_input] * 1)  # simulate top 3 predictions
    st.markdown("🎯 Find My Top College Match Now!")
    for i, pred in enumerate(predictions, 1):
        st.success(f"""
        **🏫 Option {i}:**
        - **College Code:** {pred[0]}
        - **Degree:** {pred[1]}
        - **Program:** {pred[2]}
        """)
else:
    st.info("👆 Fill in your details and click 🎯 Find My Top College Match Now!  to view results.")
