import streamlit as st
import requests
from PIL import Image
import json
from datetime import datetime

# CONFIG
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="NutriScan AI", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for NutriScan Aesthetic
st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .main {
        background-color: #0a0f0a;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Header/Footer */
    header, footer {visibility: hidden;}
    
    /* Top Navigation Bar */
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 40px;
        background-color: rgba(10, 15, 10, 0.95);
        border-bottom: 1px solid rgba(142, 214, 0, 0.1);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    .logo {
        display: flex;
        align-items: center;
        gap: 10px;
        font-weight: 800;
        font-size: 24px;
        color: #8ed600;
    }
    .nav-links {
        display: flex;
        gap: 30px;
        font-weight: 600;
        font-size: 14px;
        color: #888;
    }
    .nav-links span {
        cursor: pointer;
        transition: color 0.3s;
    }
    .nav-links span:hover, .nav-links .active {
        color: #8ed600;
    }

    /* Macro Summary Cards */
    .macro-container {
        display: flex;
        gap: 15px;
        margin-top: 80px;
        padding: 20px 0;
    }
    .macro-card {
        background: #161b16;
        padding: 10px 20px;
        border-radius: 30px;
        border: 1px solid rgba(142, 214, 0, 0.2);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .macro-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        box-shadow: 0 0 8px #8ed600;
    }
    .macro-label { font-size: 14px; font-weight: 600; }
    .macro-value { font-size: 14px; color: #888; }

    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 30px;
        background-color: #8ed600;
        color: #000000;
        border: none;
        padding: 15px;
        font-weight: 800;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(142, 214, 0, 0.3);
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(142, 214, 0, 0.6);
        background-color: #a3f500;
    }
    
    /* Capture Card */
    .capture-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0) 100%);
        border-radius: 24px;
        padding: 40px;
        border: 1px solid rgba(255,255,255,0.1);
        text-align: center;
    }
    
    /* Override Streamlit UI */
    .stTextInput>div>div>input {
        background-color: #161b16;
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
    }
    .stExpander {
        background-color: #161b16 !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 16px !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0f0a;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Custom Header
st.markdown("""
    <div class="nav-bar">
        <div class="logo">
            <span style="font-size: 28px;">🟢</span> NutriScan
        </div>
        <div class="nav-links">
            <span class="active">DASHBOARD</span>
            <span>HISTORY</span>
            <span>STATISTICS</span>
        </div>
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="color: #888; font-size: 18px;">🔔</span>
            <div style="background: #161b16; padding: 5px 15px; border-radius: 20px; border: 1px solid #333; font-size: 12px; font-weight: 600;">
                Alex Rivera
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Macro Summary Row
st.markdown("""
    <div class="macro-container">
        <div class="macro-card"><div class="macro-dot" style="background: #8ed600;"></div><span class="macro-label">1,420 kcal</span><span class="macro-value">left</span></div>
        <div class="macro-card"><div class="macro-dot" style="background: #3b82f6;"></div><span class="macro-label">65g Protein</span><span class="macro-value"></span></div>
        <div class="macro-card"><div class="macro-dot" style="background: #f59e0b;"></div><span class="macro-label">120g Carbs</span><span class="macro-value"></span></div>
    </div>
""", unsafe_allow_html=True)

st.title("Log your meal")
st.markdown("<p style='color: #888; margin-bottom: 40px;'>Choose a way to analyze your food nutrition instantly with our AI-powered recognition engine.</p>", unsafe_allow_html=True)

# Main Application Logic
user_id = "hackathon_judge_1"

col_main, col_side = st.columns([2, 1])

with col_main:
    # Capture Food Section
    st.markdown('<div class="capture-card">', unsafe_allow_html=True)
    option = st.radio("Input Method", ["Upload Image", "Camera"], horizontal=True, label_visibility="collapsed")
    
    uploaded_file = None
    if option == "Upload Image":
        uploaded_file = st.file_uploader("Drop image here or click to browse", type=["jpg", "jpeg", "png"])
    else:
        uploaded_file = st.camera_input("Point camera at your plate")

    if uploaded_file:
        st.image(uploaded_file, caption="Selected Meal", use_container_width=True)
        if st.button("Analyze Food 🚀", type="primary"):
            with st.spinner("Analyzing nutrients..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{BACKEND_URL}/analyze", files=files, params={"user_id": user_id})
                    
                    if response.status_code == 200:
                        data = response.json()
                        nutrition = data["nutrition"]
                        
                        st.session_state.last_analysis = data
                        st.success(f"Successfully Identified: **{nutrition['food_name']}**")
                    else:
                        st.error("AI Analysis failed. Please try a clearer photo.")
                except Exception as e:
                    st.error(f"Error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    # Sidebar Info & Tools
    with st.container(border=True):
        st.subheader("🤖 AI Health Assistant")
        if st.button("Consult AI Coach 🧠"):
            with st.spinner("Analyzing habits..."):
                try:
                    coach_res = requests.get(f"{BACKEND_URL}/coach/{user_id}")
                    if coach_res.status_code == 200:
                        st.session_state.coach_data = coach_res.json()
                except: st.error("Coach unavailable")
        
        if "coach_data" in st.session_state:
            coach = st.session_state.coach_data
            st.info(f"💡 {coach.get('insight')}")
            st.caption("**Suggestions:** " + ", ".join(coach.get('suggestions', [])))

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Continue on Mobile Mockup
    st.markdown("""
        <div style="background: #111; padding: 20px; border-radius: 20px; border: 1px solid #222;">
            <div style="color: #8ed600; font-size: 24px; margin-bottom: 10px;">📱</div>
            <div style="font-weight: 800; font-size: 18px;">Continue on Mobile</div>
            <div style="color: #666; font-size: 13px; margin-top: 5px;">Scan this QR code to seamlessly continue your nutrition tracking on the go.</div>
            <div style="background: white; width: 100px; height: 100px; margin: 20px auto; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                <span style="color: black; font-weight: 800; font-size: 10px;">[QR CODE]</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Recognition Results Overlay (if analyzed)
if "last_analysis" in st.session_state:
    data = st.session_state.last_analysis
    nutrition = data["nutrition"]
    
    st.divider()
    st.subheader("Recognition Results")
    res_col1, res_col2 = st.columns([1, 1.5])
    
    with res_col1:
        # Reposing the image in a results card
        st.image(uploaded_file, use_container_width=True)
    
    with res_col2:
        st.markdown(f"### {nutrition['food_name']}")
        st.markdown(f"<span style='background: rgba(142, 214, 0, 0.2); color: #8ed600; padding: 5px 12px; border-radius: 20px; font-size: 12px;'>✅ SUCCESSFULLY IDENTIFIED ({int(nutrition['confidence']*100)}% Confidence)</span>", unsafe_allow_html=True)
        
        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("Calories", f"{nutrition['calories']} kcal")
        m_col2.metric("Protein", f"{nutrition['protein_g']}g")
        m_col3.metric("Carbs", f"{nutrition['carbs_g']}g")
        m_col4.metric("Fats", f"{nutrition['fats_g']}g")
        
        if st.button("Sync Nutrition Data 🟢"):
            st.toast("Synced with Fitness App!")

st.divider()

# --- HISTORY & CHAT ---
low_col1, low_col2 = st.columns([1.5, 1])

with low_col1:
    st.subheader("🗓️ Recent Meals")
    @st.cache_data(ttl=30)
    def fetch_history(uid):
        try:
            res = requests.get(f"{BACKEND_URL}/history/{uid}")
            return res.json().get("history", [])
        except: return []
    
    history_data = fetch_history(user_id)
    if not history_data:
        st.info("Log a meal to see history")
    else:
        for item in history_data:
            with st.container(border=True):
                h_c1, h_c2, h_c3 = st.columns([3, 1, 1])
                h_c1.write(f"**{item.get('food_name')}**")
                h_c2.write(f"{item.get('calories')} kcal")
                h_c3.caption(f"🕒 {item.get('timestamp','').split('T')[1][:5] if 'T' in item.get('timestamp','') else ''}")

with low_col2:
    st.subheader("💬 NutriChat")
    with st.container(border=True, height=400):
        if "messages" not in st.session_state: st.session_state.messages = []
        for message in st.session_state.messages:
            with st.chat_message(message["role"]): st.markdown(message["content"])

        # Voice/Text Input
        audio_file = st.audio_input("Record Voice 🎙️", label_visibility="collapsed")
        if audio_file:
            with st.spinner("AI listening..."):
                try:
                    files = {"file": (audio_file.name, audio_file.getvalue(), audio_file.type)}
                    res = requests.post(f"{BACKEND_URL}/voice_chat/{user_id}", files=files)
                    if res.status_code == 200:
                        answer = res.json()["response"]
                        st.session_state.messages.append({"role": "user", "content": "🎤 (Voice Message)"})
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                        st.rerun()
                except: st.error("Voice fail")

        if prompt := st.chat_input("Ask anything..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(f"{BACKEND_URL}/chat/{user_id}", json={"message": prompt})
                    if response.status_code == 200:
                        st.session_state.messages.append({"role": "assistant", "content": response.json()["response"]})
                        st.rerun()
                except: st.error("Chat fail")
