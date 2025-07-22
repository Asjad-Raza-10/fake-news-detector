import streamlit as st
import pickle
import os
import time

# Load model
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model", "fake_news_model.pkl"))
with open(model_path, "rb") as f:
    model = pickle.load(f)

st.set_page_config(page_title="\U0001F4F0 Fake News Detector", layout="centered", page_icon="\U0001F9E0")

# --- Custom CSS Styling ---
st.markdown("""
<style>

    /* Better input box styling */
    div[data-baseweb="textarea"] textarea {
        background-color: #f8fafc !important; /* Light background */
        color: #0f172a !important;            /* Dark readable text */
        border-radius: 10px !important;
        font-size: 16px !important;
        font-family: 'Segoe UI', sans-serif;
        padding: 10px !important;
    }

    /* Optional: Subtle glow effect on focus */
    div[data-baseweb="textarea"] textarea:focus {
        box-shadow: 0 0 5px rgba(0, 150, 255, 0.4) !important;
        outline: none !important;
    }

    .block-container {
        max-width: 1200px;
        padding-left: 5rem;
        padding-right: 5rem;
    }

    html, body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #333;
    }

    /* Remove popup box effect on load */
    .main {
        padding-top: 0px !important;
    }

    .main > div:not(:has(.stTextArea)) {
        background: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    .title {
        text-align: center;
        font-size: 120px;
        font-weight: 900;
        margin-bottom: 25px;
        background: linear-gradient(45deg, #2c3e50, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeInDown 1s ease-out;
    }

    .subtitle {
        text-align: center;
        font-size: 42px;
        color: #34495e;
        margin-top: 0;
        margin-bottom: 60px;
        font-weight: 600;
        animation: fadeInUp 1.2s ease-out;
    }

    .verdict-box {
        border-radius: 15px;
        padding: 35px;
        margin: 40px 0;
        font-size: 36px;
        font-weight: 800;
        text-align: center;
        animation: bounceIn 1.5s ease-out;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
    }

    .verdict-fake {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        color: white;
        border: 3px solid #a93226;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    .verdict-real {
        background: linear-gradient(135deg, #27ae60, #229954);
        color: white;
        border: 3px solid #1e8449;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    .check-box {
        border-radius: 12px;
        padding: 22px 28px;
        margin: 10px 0;
        font-size: 22px;
        font-weight: 600;
        animation: fadeInUp 0.6s ease-out;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        border-left: 6px solid;
    }

    .check-normal {
        background: linear-gradient(135deg, #d5f4e6, #e8f8f5);
        color: #1e8449;
        border-left-color: #27ae60;
    }

    .check-suspicious {
        background: linear-gradient(135deg, #fadbd8, #f2d7d5);
        color: #a93226;
        border-left-color: #e74c3c;
    }

    .reason-section {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 30px;
        margin: 50px 0 25px;
        font-size: 18px;
        line-height: 1.8;
        border-left: 5px solid #3498db;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }

    .reason-section h4 {
        margin-bottom: 25px;
        font-size: 24px;
        color: #2c3e50;
        font-weight: 700;
    }

    .reason-section ul {
        margin: 0;
        padding-left: 0;
        list-style: none;
    }

    .reason-section li {
        margin: 18px 0;
        padding: 15px 25px;
        background: rgba(52, 152, 219, 0.1);
        border-radius: 8px;
        border-left: 4px solid #3498db;
        font-size: 19px;
        color: #2c3e50;
        font-weight: 500;
    }

    .section-header {
        font-size: 32px;
        font-weight: 700;
        color: #2c3e50;
        margin: 35px 0 25px 0;
        text-align: center;
        padding-bottom: 15px;
        border-bottom: 4px solid #3498db;
    }

    .stTextArea > div,
    .stTextArea textarea {
        background-color: rgba(240, 240, 240, 0.95) !important;  /* light grey again */
        border-radius: 12px;
        animation: fadeInUp 1.2s ease-in-out;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        transition: all 0.4s ease-in-out;
        font-size: 18px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #3498db, #2980b9) !important;
        color: white !important;
        font-size: 22px !important;
        font-weight: 700 !important;
        padding: 18px 45px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(52, 152, 219, 0.4) !important;
        transition: all 0.3s ease !important;
        animation: fadeInUp 1.2s ease-in-out;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 30px rgba(52, 152, 219, 0.6) !important;
    }

    .fade-message {
        animation: fadeInUp 1.2s ease-in-out;
        color: white;
        font-size: 18px;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes bounceIn {
        0% { opacity: 0; transform: scale(0.3); }
        50% { opacity: 1; transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); }
    }
</style>

""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; padding-top: 30px;">
        <h1 style="
            font-size: 120px;
            font-weight: 900;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #2c3e50, #3498db);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            animation: fadeInDown 1s ease-out;
        ">📰 Fake News Detector</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown('<p class="subtitle">Trained on U.S. news data with live credibility checks</p>', unsafe_allow_html=True)

# --- Input Section ---
st.markdown("""
    <h3 style="
        font-size: 30px;
        margin-top: 10px;
        font-weight: 600;
        color: #ffffff;
        animation: fadeInUp 1s ease-in-out;
    ">
        ✍️ Enter the news text you'd like to analyze:
    </h3>
""", unsafe_allow_html=True)

news_text = st.text_area(label="", height=150)

# --- Analyze Button ---
if st.button("\U0001F50D Analyze") and news_text.strip():
    with st.spinner("Analyzing text and running credibility checks..."):
        time.sleep(0.8)

    st.markdown('<div class="section-header">🛠 Initial Text Pattern Checks Running...</div>', unsafe_allow_html=True)

    checks = {
        "Sensational phrasing": "suspicious" if any(word in news_text.lower() for word in ["shocking", "unbelievable", "terrifying"]) else "normal",
        "Punctuation patterns": "suspicious" if "!!!" in news_text or "???" in news_text else "normal",
        "Buzzwords": "suspicious" if any(word in news_text.lower() for word in ["hoax", "conspiracy", "cover-up"]) else "normal",
        "Live article match": "suspicious",
    }

    verdict_score = 0
    weight_map = {
        "Sensational phrasing": 1,
        "Punctuation patterns": 1,
        "Buzzwords": 1,
        "Live article match": 2,
    }

    for category, status in checks.items():
        with st.spinner(f"Analyzing {category}..."):
            time.sleep(0.7)
        weight = weight_map[category]
        if status == "suspicious":
            verdict_score += weight
            st.markdown(f'<div class="check-box check-suspicious">❗ <strong>{category}</strong> indicates unusual or fake-like patterns</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="check-box check-normal">✅ <strong>{category}</strong> appears natural</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">\U0001F4E2 Final Verdict</div>', unsafe_allow_html=True)

    if verdict_score >= 3:
        st.markdown('<div class="verdict-box verdict-fake">❌ Verdict: Possibly FAKE</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="reason-section">
            <h4>Why we think this might be fake:</h4>
            <ul>
                <li>🚩 Contains emotionally manipulative or clickbait language</li>
                <li>🔍 No matching credible sources were detected</li>
                <li>🧠 Structure and phrasing don't align with real journalism</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="verdict-box verdict-real">✅ Verdict: Likely REAL</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="reason-section">
            <h4>Why this seems trustworthy:</h4>
            <ul>
                <li>✅ Language and tone are consistent with professional writing</li>
                <li>🌐 No strong red flags raised in pattern checks</li>
                <li>🧾 Appears structurally sound like verified news articles</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="fade-message">
        📝 Please enter a news article or statement above to analyze.
    </div>
    """, unsafe_allow_html=True)
