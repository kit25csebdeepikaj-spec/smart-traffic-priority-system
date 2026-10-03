# app.py
import streamlit as st
import time

# Page Configuration
st.set_page_config(
    page_title="Traffic Signal Control Dashboard",
    page_icon="🚦",
    layout="wide"
)

# Custom Styling for clean presentation
st.markdown("""
    <style>
    .metric-box {
        background-color: #1e293b;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-title {
        font-size: 15px;
        color: #94a3b8;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
    }
    .timer-text {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚦 Junction Signal State Dashboard")
st.markdown("---")

st.subheader("All Lanes Status Overview")

# Create 4 columns for North, South, East, and West
cols = st.columns(4)

# Direction data mapping
directions = [
    {"name": "North", "status": "RED", "color": "#ef4444", "timer": "30s"},
    {"name": "South", "status": "RED", "color": "#ef4444", "timer": "30s"},
    {"name": "East", "status": "RED", "color": "#ef4444", "timer": "30s"},
    {"name": "West", "status": "GREEN", "color": "#22c55e", "timer": "30s"}
]

for i, dir_info in enumerate(directions):
    with cols[i]:
        st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Active Direction</div>
                <div style="font-size: 18px; font-weight: bold; color: #f8fafc; margin-bottom: 8px;">{dir_info['name']}</div>
                <div class="metric-title">Signal Light Status</div>
                <div class="metric-value" style="color: {dir_info['color']};">{dir_info['status']}</div>
                <div class="timer-text">State Timer Countdown: {dir_info['timer']}</div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.info("System Status: West corridor priority active. All other lanes held at RED.")

# Auto-refresh mechanism
time.sleep(1)
st.rerun()