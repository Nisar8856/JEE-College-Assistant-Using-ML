# this is for multiplecolleg code
import streamlit as st
import pickle

# Set page configuration
st.set_page_config(page_title="🎯 JEE College Assistant", layout="centered")

# Load your trained model
model = pickle.load(open("model1.pkl", "rb"))

# Inject custom CSS
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
st.markdown("<h1 style='text-align: center; color: #facc15;'>🎓 JEE College Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Predict your best-fit colleges based on rank and preferences</p>", unsafe_allow_html=True)

# Sidebar inputs
st.sidebar.image("logo1.png", use_container_width=True)
st.sidebar.title("📌 Input Your Details")

category = st.sidebar.selectbox("Category", ["General", "OBC", "SC", "ST", "EWS"])
quota = st.sidebar.selectbox("Quota", ["AI", "HS", "OS"])
pool = st.sidebar.selectbox("Gender Pool", ["Gender-Neutral", "Female-only"])
institute_type = st.sidebar.selectbox("Institute Type", ["NIT", "IIT"])
round_no = st.sidebar.selectbox("Round Number", list(range(1, 7)))
opening_rank = st.sidebar.number_input("Opening Rank", min_value=1, max_value=500000, value=2000)
closing_rank = st.sidebar.number_input("Closing Rank", min_value=1, max_value=500000, value=2841)

# Encode inputs
encoded_input = [
    0 if category == "General" else 1 if category == "OBC" else 2 if category == "SC" else 3 if category == "ST" else 4,
    0 if quota == "AI" else 1 if quota == "HS" else 2,
    0 if pool == "Gender-Neutral" else 1,
    1 if institute_type == "NIT" else 0,
    round_no,
    opening_rank,
    closing_rank
]

# Predict button
st.markdown("<hr style='border: 1px solid #374151;'>", unsafe_allow_html=True)

if st.button("🎯 Predict Top 3 Colleges"):
    predictions = []
    seen = set()

    # Generate 3 slightly varied inputs to get unique results
    for offset in [0, 500, 1000]:
        test_input = encoded_input.copy()
        test_input[5] = min(500000, opening_rank + offset)
        test_input[6] = min(500000, closing_rank + offset)

        prediction = model.predict([test_input])[0]  # Predict returns [College, Degree, Program]
        college_key = tuple(prediction)

        if college_key not in seen:
            seen.add(college_key)
            predictions.append(prediction)

        if len(predictions) == 3:
            break

    if predictions:
        st.markdown("### st🎓 Top 3 Predicted Colleges")
        for i, pred in enumerate(predictions, 1):
            st.success(f"""
            **🏫 Option {i}:**
            - **College:** {pred[0]}
            - **Degree:** {pred[1]}
            - **Program:** {pred[2]}
            """)
    else:
        st.warning("⚠️ Unable to find 3 distinct college predictions. Try modifying rank range.")

else:
    st.info("👆 Fill in your details and click **Predict Top 3 Colleges** to view results.")
