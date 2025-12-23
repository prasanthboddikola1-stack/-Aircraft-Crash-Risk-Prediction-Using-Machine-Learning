import streamlit as st
from model import predict_by_record_id

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="✈️ Aircraft Crash Risk Prediction",
    layout="centered"
)

# ================= SESSION STATE =================
if "page" not in st.session_state:
    st.session_state.page = "input"

if "result" not in st.session_state:
    st.session_state.result = None

# ================= GLOBAL STYLING =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0f2fe, #f8fafc);
}

.block-container {
    padding-top: 2.5rem;
    max-width: 850px;
}

h1 {
    font-size: 3rem;
    font-weight: 800;
    color: #0b2c4d;
}

.tagline {
    font-size: 1.3rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 2rem;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 18px;
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 14px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
}

.low { border-left: 8px solid #22c55e; }
.medium { border-left: 8px solid #facc15; }
.high { border-left: 8px solid #ef4444; }

div.stButton > button {
    background: linear-gradient(135deg, #0b2c4d, #143a5a);
    color: white;
    font-weight: 700;
    padding: 0.8rem 1.8rem;
    border-radius: 14px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# PAGE 1 : INPUT PAGE
# ==================================================
if st.session_state.page == "input":

    st.title("✈️ Aircraft Crash Risk Prediction")
    st.markdown(
        "<div class='tagline'>✨ Welcome on board — your AI co-pilot for safer skies ✈️</div>",
        unsafe_allow_html=True
    )

    record_id = st.number_input(
        "🆔 Enter Flight Record Number",
        min_value=0,
        step=1
    )

    if st.button("🔍 Get Risk Assessment"):
        result = predict_by_record_id(int(record_id))

        if result is None:
            st.error("❌ Invalid flight record number")
        else:
            st.session_state.result = result
            st.session_state.page = "result"
            st.rerun()

# ==================================================
# PAGE 2 : RESULT PAGE
# ==================================================
elif st.session_state.page == "result":

    result = st.session_state.result

    st.title("🛫 Flight Risk Report")
    st.markdown(
        "<div class='tagline'>💙 Have a safe flight — safety begins with awareness ✨</div>",
        unsafe_allow_html=True
    )

    # -------- FLIGHT DETAILS --------
    st.subheader("✈️ Flight Information")

    st.markdown(f"""
    <div class="card">✈️ Airline: <b>{result["Airline"]}</b></div>
    <div class="card">📍 Route: <b>{result["Source"]} → {result["Destination"]}</b></div>
    <div class="card">💨 Wind Speed: <b>{result["Wind"]} km/h</b></div>
    <div class="card">👁️ Visibility: <b>{result["Visibility"]} km</b></div>
    <div class="card">⛈️ Storm Condition: <b>{result["Storm"]}</b></div>
    """, unsafe_allow_html=True)

    # -------- RISK SECTION --------
    st.subheader("⚠️ Risk Intelligence")

    risk = result["Risk_Level"]

    if risk == "LOW":
        risk_class = "low"
        msg = "✅ Safe for operation — cleared for flight"
    elif risk == "MEDIUM":
        risk_class = "medium"
        msg = "⚠️ Moderate risk — monitoring recommended"
    else:
        risk_class = "high"
        msg = "🚨 High risk — delay or reroute advised"

    st.markdown(f"""
    <div class="card {risk_class}">
        🚦 Risk Level: <b>{risk}</b>
    </div>
    <div class="card {risk_class}">
        📊 Crash Probability: <b>{result["Crash_Probability"]}%</b>
    </div>
    """, unsafe_allow_html=True)

    if risk == "LOW":
        st.success(msg)
    elif risk == "MEDIUM":
        st.warning(msg)
    else:
        st.error(msg)

    if st.button("⬅️ Check Another Flight"):
        st.session_state.page = "input"
        st.rerun()
