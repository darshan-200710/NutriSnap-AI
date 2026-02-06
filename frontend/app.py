import streamlit as st
import requests
from PIL import Image
import json

# CONFIG
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="NutriSnap AI", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    .stButton>button {
        border-radius: 12px;
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 43, 0.3);
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        text-align: center;
    }
    .stMarkdown h1 {
        color: #1a1a1a;
        font-weight: 800;
    }
    .sidebar .sidebar-content {
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍎 NutriSnap: AI Food Analyzer")
st.markdown("Upload a photo of your meal to get instant nutrition insights.")

# Sidebar
with st.sidebar:
    st.header("Project Info")
    st.info("Team: 4 Devs\nStack: FastAPI + Streamlit + Firebase + Gemini")
    st.checkbox("Enable Fitness Sync", value=True, key="sync_enabled")
    
    user_id = "hackathon_judge_1"
    
    if st.button("Refresh History 🔄"):
        st.cache_data.clear()

# Main Content
col1, col2 = st.columns(2)

uploaded_file = None

with col1:
    st.subheader("1. Capture Food")
    option = st.radio("Input Method", ["Upload Image", "Camera"])
    
    if option == "Upload Image":
        uploaded_file = st.file_uploader("Choose a food image...", type=["jpg", "jpeg", "png"])
    else:
        uploaded_file = st.camera_input("Take a picture")

    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

with col2:
    st.subheader("2. Analysis Results")
    
    if uploaded_file:
        if st.button("Analyze Nutrition 🚀", type="primary"):
            with st.spinner("Asking AI Chef..."):
                try:
                    # Prepare file for API
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    user_id = "hackathon_judge_1"
                    
                    response = requests.post(f"{BACKEND_URL}/analyze", files=files, params={"user_id": user_id})
                    
                    if response.status_code == 200:
                        data = response.json()
                        nutrition = data["nutrition"]
                        
                        # Display Cards
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Calories", f"{nutrition['calories']} kcal")
                        c2.metric("Protein", f"{nutrition['protein_g']}g")
                        c3.metric("Carbs", f"{nutrition['carbs_g']}g")
                        c4.metric("Fats", f"{nutrition['fats_g']}g")
                        
                        st.success(f"Identified: **{nutrition['food_name']}**")
                        
                        with st.expander("debug raw response"):
                             st.json(data)
                             
                        if data.get("fitness_sync_status"):
                            st.toast("✅ Synced with Fitness Platform!", icon="🏃")
                            
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                        
                except Exception as e:
                    st.error(f"Connection Error: {e}")
                    st.warning("Make sure Backend is running on port 8000")

st.divider()

# --- HISTORY SECTION ---
st.subheader("🗓️ Recent Meals")

@st.cache_data(ttl=60)
def fetch_history(uid):
    try:
        res = requests.get(f"{BACKEND_URL}/history/{uid}")
        if res.status_code == 200:
            return res.json().get("history", [])
    except:
        return []
    return []

history_data = fetch_history(user_id)

if not history_data:
    st.info("No meals logged yet. Analysis some food to see them here!")
else:
    # Display as a table or cards
    for item in history_data:
        cols = st.columns([2, 1, 1, 1, 1])
        with cols[0]:
            st.write(f"**{item.get('food_name', 'Unknown')}**")
        with cols[1]:
            st.write(f"{item.get('calories', 0)} kcal")
        with cols[2]:
            st.write(f"P: {item.get('nutrition', {}).get('protein_g', 0)}g")
        with cols[3]:
            st.write(f"C: {item.get('nutrition', {}).get('carbs_g', 0)}g")
        with cols[4]:
            # Format timestamp
            ts = item.get('timestamp', '')
            if ts:
                try:
                    time_str = ts.split('T')[1].split('.')[0] # HH:MM:SS
                    st.caption(f"🕒 {time_str}")
                except:
                    st.caption(ts)
        st.divider()
