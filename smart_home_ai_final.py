"""
FINALIZED Smart Home AI Dashboard with LangGraph Integration
Combines DQN Reinforcement Learning + Gemini AI Agent
"""
import streamlit as st
import pandas as pd
import numpy as np
from stable_baselines3 import DQN
from environment import SmartHomeEnv
import plotly.graph_objects as go
import plotly.express as px
import time
import random
import os

# Import LangGraph agent
try:
    from langgraph_agent import get_ai_recommendation, chat_with_agent
    LANGGRAPH_AVAILABLE = True
except Exception as e:
    LANGGRAPH_AVAILABLE = False
    st.warning(f"⚠️ LangGraph not available: {e}")

st.set_page_config(page_title="🤖 Smart Home AI Dashboard", layout="wide", page_icon="🏠")

# Enhanced CSS
st.markdown("""
<style>
    .big-font {
        font-size:24px !important;
        font-weight: bold;
        color: #1f77b4;
    }
    .highlight-box {
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        background-color: #f0f8f0;
        margin: 10px 0px;
    }
    .warning-box {
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff9800;
        background-color: #fff8f0;
        margin: 10px 0px;
    }
    .ai-box {
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #2196F3;
        background-color: #e3f2fd;
        margin: 10px 0px;
    }
    .agent-box {
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #9C27B0;
        background-color: #f3e5f5;
        margin: 10px 0px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'step_count' not in st.session_state:
    st.session_state.step_count = 0

# Helper function to safely extract scalar values
def safe_float(value):
    """Convert numpy array or scalar to float"""
    if isinstance(value, (np.ndarray, list)):
        return float(np.asarray(value).flatten()[0])
    return float(value)

# Load trained DQN model
@st.cache_resource
def load_model():
    model_paths = [
        "smart_home_ai_brain.zip",
        "../smart_home_ai_brain.zip",
        r"d:\SmartHomeAI-main\smart_home_ai_brain.zip"
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            try:
                return DQN.load(path, print_system_info=False)
            except Exception as e:
                st.error(f"Model load error: {e}")
                # Create dummy model for demo
                return None
    return None

# Load environment
@st.cache_resource
def load_environment():
    try:
        return SmartHomeEnv(data_file="SmartHome_Realistic_Dataset.csv")
    except:
        st.warning("⚠️ Using simulated environment")
        return None

# Header
st.title("🤖 Smart Home AI Control Dashboard")
st.markdown("### 🧠 Powered by DQN Reinforcement Learning + Gemini LangGraph Agent")

# Sidebar controls
st.sidebar.header("🎛️ Control Panel")
mode = st.sidebar.radio(
    "Select Mode:",
    ["🤖 AI Agent Mode", "🎮 Manual Control", "📊 Analytics"],
    index=0
)

# Load resources
model = load_model()
env = load_environment()

if env is None:
    # Simulated environment
    st.info("📌 Running in simulation mode")
    obs = np.array([24.0, 60.0, 8.0, 0.8, 1.0, 50.0, 2.0])
else:
    obs = env.reset()
    # Handle tuple return from reset (obs, info)
    if isinstance(obs, tuple):
        obs = obs[0]
    # Flatten if nested
    obs = np.asarray(obs).flatten()

# ====================
# AI AGENT MODE
# ====================
if mode == "🤖 AI Agent Mode":
    st.header("🤖 Intelligent Agent Control")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Current Environment State")
        
        # Display current state
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        with metrics_col1:
            temp = safe_float(obs[0])
            st.metric("🌡️ Temperature", f"{temp:.1f}°C", 
                     delta=f"{temp-22:.1f}°C from optimal")
        
        with metrics_col2:
            humidity = safe_float(obs[1])
            st.metric("💧 Humidity", f"{humidity:.0f}%")
        
        with metrics_col3:
            occupancy = int(safe_float(obs[2]) > 5)
            st.metric("👥 Occupancy", "Present" if occupancy else "Away")
        
        with metrics_col4:
            energy = safe_float(obs[6])
            st.metric("⚡ Energy", f"{energy:.2f} kWh")
        
        # Visual gauges
        fig_gauges = go.Figure()
        
        fig_gauges.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=temp,
            title={'text': "Temperature (°C)"},
            delta={'reference': 22},
            gauge={
                'axis': {'range': [15, 35]},
                'bar': {'color': "darkred" if temp > 26 else "darkblue" if temp < 20 else "green"},
                'steps': [
                    {'range': [15, 20], 'color': "lightblue"},
                    {'range': [20, 26], 'color': "lightgreen"},
                    {'range': [26, 35], 'color': "lightcoral"}
                ]
            },
            domain={'x': [0, 0.45], 'y': [0, 1]}
        ))
        
        fig_gauges.add_trace(go.Indicator(
            mode="gauge+number",
            value=humidity,
            title={'text': "Humidity (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "blue"},
                'steps': [
                    {'range': [0, 40], 'color': "lightyellow"},
                    {'range': [40, 70], 'color': "lightblue"},
                    {'range': [70, 100], 'color': "lightcoral"}
                ]
            },
            domain={'x': [0.55, 1], 'y': [0, 1]}
        ))
        
        fig_gauges.update_layout(height=300)
        st.plotly_chart(fig_gauges, use_container_width=True)
    
    with col2:
        st.subheader("🎛️ Current Status")
        
        hvac_status = bool(safe_float(obs[4]))
        lighting = safe_float(obs[5])
        comfort = safe_float(obs[3])
        
        st.info(f"**HVAC:** {'🟢 ON' if hvac_status else '🔴 OFF'}")
        st.info(f"**Lighting:** {lighting:.0f}%")
        st.info(f"**Comfort:** {comfort:.2f}")
        
        # Agent decision button
        st.markdown("---")
        if st.button("🧠 Get AI Recommendation", use_container_width=True):
            if LANGGRAPH_AVAILABLE:
                with st.spinner("🤖 AI Agent analyzing..."):
                    current_state = {
                        "temperature": safe_float(obs[0]),
                        "humidity": safe_float(obs[1]),
                        "occupancy": int(safe_float(obs[2]) > 5),
                        "time_of_day": int(safe_float(obs[2])) if safe_float(obs[2]) <= 24 else 12,
                        "hvac_status": int(safe_float(obs[4])),
                        "lighting": safe_float(obs[5]),
                        "energy_usage": safe_float(obs[6])
                    }
                    
                    recommendation = get_ai_recommendation(current_state)
                    
                    st.session_state.last_recommendation = recommendation
            else:
                st.error("LangGraph not available")
    
    # Display AI recommendation
    if hasattr(st.session_state, 'last_recommendation'):
        st.markdown("---")
        st.subheader("🧠 Gemini AI Agent Analysis")
        
        rec = st.session_state.last_recommendation
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown(f"""
            <div class="agent-box">
            <h4>💡 Recommendation</h4>
            <p style="font-size:18px; font-weight:bold;">{rec['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_b:
            st.markdown(f"""
            <div class="ai-box">
            <h4>🧠 Reasoning</h4>
            <p>{rec['reasoning']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if rec.get('analysis'):
            st.markdown(f"""
            <div class="highlight-box">
            <h4>📊 Detailed Analysis</h4>
            <p>{rec['analysis']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # DQN Model prediction
    st.markdown("---")
    st.subheader("🎯 DQN Model Action")
    
    if model:
        action, _ = model.predict(obs, deterministic=True)
        action_names = ["Do Nothing", "Turn HVAC On", "Turn HVAC Off", 
                       "Increase Light", "Decrease Light"]
        
        st.success(f"**DQN Recommends:** {action_names[action]}")
    else:
        st.warning("⚠️ Model not available - using simulated decisions")
    
    # Chat with AI
    st.markdown("---")
    st.subheader("💬 Chat with AI Assistant")
    
    user_input = st.text_input("Ask about your smart home:", 
                               placeholder="e.g., Why is the temperature high?")
    
    if user_input and st.button("Send"):
        if LANGGRAPH_AVAILABLE:
            current_state = {
                "temperature": safe_float(obs[0]),
                "humidity": safe_float(obs[1]),
                "occupancy": int(safe_float(obs[2]) > 5),
                "hvac_status": int(safe_float(obs[4])),
                "lighting": safe_float(obs[5]),
                "energy_usage": safe_float(obs[6])
            }
            
            response = chat_with_agent(user_input, current_state)
            st.session_state.chat_history.append({"user": user_input, "ai": response})
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("#### 💬 Conversation History")
        for chat in st.session_state.chat_history[-5:]:
            st.markdown(f"**You:** {chat['user']}")
            st.markdown(f"**AI:** {chat['ai']}")
            st.markdown("---")

# ====================
# MANUAL CONTROL MODE
# ====================
elif mode == "🎮 Manual Control":
    st.header("🎮 Manual Smart Home Control")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌡️ Climate Control")
        hvac_control = st.radio("HVAC Status:", ["Off", "On"])
        target_temp = st.slider("Target Temperature:", 18, 30, 22)
        
        st.subheader("💡 Lighting Control")
        light_level = st.slider("Light Level:", 0, 100, 50)
    
    with col2:
        st.subheader("📊 Current Readings")
        st.metric("Temperature", f"{safe_float(obs[0]):.1f}°C")
        st.metric("Humidity", f"{safe_float(obs[1]):.0f}%")
        st.metric("Energy Usage", f"{safe_float(obs[6]):.2f} kWh")
        
        if st.button("Apply Changes", use_container_width=True):
            st.success("✅ Settings applied!")
            st.balloons()

# ====================
# ANALYTICS MODE
# ====================
else:
    st.header("📊 Smart Home Analytics")
    
    # Generate sample data
    hours = np.arange(24)
    temps = 22 + 4 * np.sin(hours * np.pi / 12) + np.random.randn(24) * 0.5
    energy = 1.5 + 2 * np.random.rand(24)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌡️ Temperature Trend")
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x=hours, y=temps, mode='lines+markers',
                                      name='Temperature', line=dict(color='red', width=2)))
        fig_temp.update_layout(xaxis_title="Hour", yaxis_title="Temperature (°C)", height=300)
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Energy Consumption")
        fig_energy = go.Figure()
        fig_energy.add_trace(go.Bar(x=hours, y=energy, name='Energy',
                                    marker_color='green'))
        fig_energy.update_layout(xaxis_title="Hour", yaxis_title="Energy (kWh)", height=300)
        st.plotly_chart(fig_energy, use_container_width=True)
    
    # Statistics
    st.subheader("📈 Daily Statistics")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Avg Temp", f"{temps.mean():.1f}°C")
    with stat_col2:
        st.metric("Max Temp", f"{temps.max():.1f}°C")
    with stat_col3:
        st.metric("Total Energy", f"{energy.sum():.2f} kWh")
    with stat_col4:
        st.metric("AI Decisions", st.session_state.step_count)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🤖 <b>Smart Home AI Dashboard</b> | Powered by DQN + Gemini AI LangGraph Agent</p>
    <p>Built with Streamlit, Stable-Baselines3, LangGraph & Google Gemini</p>
</div>
""", unsafe_allow_html=True)
