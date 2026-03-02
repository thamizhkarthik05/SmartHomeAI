"""
REAL-TIME Smart Home AI Dashboard with Live Simulation
Continuous environment updates with DQN + Gemini AI Agent
"""
import streamlit as st
import pandas as pd
import numpy as np
from stable_baselines3 import DQN
from interactive_environment import InteractiveSmartHomeEnv  # Use interactive environment with working actions!
import plotly.graph_objects as go
import plotly.express as px
import time
import random
import os
from datetime import datetime

# Import LangGraph agent
try:
    from langgraph_agent import (get_ai_recommendation, chat_with_agent, 
                                  add_manual_override, get_memory_stats, 
                                  should_auto_apply, detect_confident_patterns)
    LANGGRAPH_AVAILABLE = True
except Exception as e:
    LANGGRAPH_AVAILABLE = False
    print(f"LangGraph not available: {e}")

st.set_page_config(page_title="🤖 Smart Home AI - Live Simulation", layout="wide", page_icon="🏠")

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
        color: #1a1a1a;
    }
    .highlight-box h4 {
        color: #2d5016;
        margin-top: 0;
    }
    .highlight-box p {
        color: #1a1a1a;
        margin-bottom: 0;
    }
    .warning-box {
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff9800;
        background-color: #fff8f0;
        margin: 10px 0px;
        color: #1a1a1a;
    }
    .ai-box {
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #2196F3;
        background-color: #e3f2fd;
        margin: 10px 0px;
        color: #1a1a1a;
    }
    .ai-box h4 {
        color: #0d47a1;
        margin-top: 0;
    }
    .ai-box p {
        color: #1a1a1a;
        margin-bottom: 0;
    }
    .agent-box {
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #9C27B0;
        background-color: #f3e5f5;
        margin: 10px 0px;
        color: #1a1a1a;
    }
    .agent-box h4 {
        color: #4a148c;
        margin-top: 0;
    }
    .agent-box p {
        color: #1a1a1a;
        margin-bottom: 0;
    }
    .live-indicator {
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False
if 'step_count' not in st.session_state:
    st.session_state.step_count = 0
if 'history' not in st.session_state:
    st.session_state.history = {
        'temperature': [],
        'humidity': [],
        'energy': [],
        'actions': [],
        'rewards': [],
        'timestamps': [],
        'comfort': [],
        'lighting': []
    }
if 'current_obs' not in st.session_state:
    st.session_state.current_obs = None
if 'last_action' not in st.session_state:
    st.session_state.last_action = 0
if 'last_reward' not in st.session_state:
    st.session_state.last_reward = 0
if 'ai_analysis' not in st.session_state:
    st.session_state.ai_analysis = None
if 'total_reward' not in st.session_state:
    st.session_state.total_reward = 0
if 'last_action_source' not in st.session_state:
    st.session_state.last_action_source = "DQN"  # "DQN" or "Manual"

# Helper function
def safe_float(value):
    """Convert numpy array or scalar to float"""
    if isinstance(value, (np.ndarray, list)):
        return float(np.asarray(value).flatten()[0])
    return float(value)

def explain_dqn_decision(obs, action, reward):
    """Explain why DQN chose this action"""
    temp = safe_float(obs[0])
    humidity = safe_float(obs[1])
    time_of_day = safe_float(obs[2])
    comfort = safe_float(obs[3])
    hvac_on = bool(safe_float(obs[4]))
    lighting = safe_float(obs[5])
    energy = safe_float(obs[6])
    
    explanations = []
    
    action_names = {
        0: "⏸️ Do Nothing",
        1: "❄️ Turn HVAC On",
        2: "🔥 Turn HVAC Off",
        3: "💡 Increase Lighting",
        4: "🌙 Decrease Lighting"
    }
    
    explanations.append(f"**Action Taken:** {action_names.get(action, 'Unknown')}")
    
    # Temperature reasoning
    if action == 1:  # HVAC ON
        explanations.append(f"🌡️ Temperature is {temp:.1f}°C → Needs cooling/heating")
        if temp > 26:
            explanations.append("   → Room is getting warm, HVAC will cool")
        elif temp < 20:
            explanations.append("   → Room is getting cold, HVAC will heat")
    elif action == 2:  # HVAC OFF
        explanations.append(f"🌡️ Temperature is {temp:.1f}°C → Comfortable range")
        explanations.append("   → Turning off HVAC to save energy")
    
    # Lighting reasoning
    if action == 3:  # Increase light
        explanations.append(f"💡 Lighting at {lighting:.0f}% → Too dim")
        hour = int(time_of_day)
        if 6 <= hour < 22:
            explanations.append("   → Daytime needs more brightness")
    elif action == 4:  # Decrease light
        explanations.append(f"💡 Lighting at {lighting:.0f}% → Too bright")
        explanations.append("   → Reducing to save energy")
    
    # Do nothing reasoning
    if action == 0:
        explanations.append(f"✅ **Optimal conditions** - maintaining current state")
        explanations.append(f"   → Temperature: {temp:.1f}°C | Comfort: {comfort:.2f}")
    
    # Reward explanation
    if reward > 5:
        explanations.append(f"🎉 **Excellent! (+{reward:.1f})** High comfort, low energy")
    elif reward > 0:
        explanations.append(f"✅ **Good (+{reward:.1f})** Balanced decision")
    elif reward > -3:
        explanations.append(f"⚠️ **Minor penalty ({reward:.1f})** Small inefficiency")
    else:
        explanations.append(f"❌ **Poor ({reward:.1f})** Discomfort or waste")
    
    return explanations

def get_ideal_conditions(time_of_day):
    """Get ideal conditions based on time"""
    hour = int(time_of_day)
    
    if 22 <= hour or hour < 6:  # Night
        return {
            'temp_range': "20-23°C",
            'light_range': "0-20%",
            'activity': '😴 Sleeping',
            'priority': 'Low energy, dark'
        }
    elif 6 <= hour < 9:  # Morning
        return {
            'temp_range': "21-24°C",
            'light_range': "60-80%",
            'activity': '☀️ Waking up',
            'priority': 'Moderate light'
        }
    elif 9 <= hour < 17:  # Day
        return {
            'temp_range': "22-25°C",
            'light_range': "70-95%",
            'activity': '💼 Working',
            'priority': 'Good lighting'
        }
    else:  # Evening
        return {
            'temp_range': "21-24°C",
            'light_range': "50-70%",
            'activity': '🌆 Relaxing',
            'priority': 'Comfort focus'
        }

# Load trained DQN model
@st.cache_resource
def load_model():
    model_paths = [
        "smart_home_ai_brain_v2.zip",      # NEW improved model first!
        "smart_home_ai_brain.zip",         # Fallback to old model
        "../smart_home_ai_brain_v2.zip",
        "../smart_home_ai_brain.zip",
        r"d:\SmartHomeAI-main\smart_home_ai_brain_v2.zip",
        r"d:\SmartHomeAI-main\smart_home_ai_brain.zip"
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            try:
                model = DQN.load(path, print_system_info=False)
                st.success(f"✅ Loaded model: {os.path.basename(path)}")
                return model
            except:
                pass
    return None

# Load environment
@st.cache_resource
def load_environment():
    try:
        return InteractiveSmartHomeEnv()  # Interactive environment with working actions!
    except Exception as e:
        st.error(f"Environment error: {e}")
        return None

# Action names
ACTION_NAMES = {
    0: "⏸️ Do Nothing",
    1: "❄️ Turn HVAC On",
    2: "🔥 Turn HVAC Off",
    3: "💡 Increase Lighting",
    4: "🌙 Decrease Lighting"
}

# Header
st.title("🤖 Smart Home AI - Live Simulation Dashboard")
st.markdown("### 🔴 Real-Time Environment Monitoring with DQN + Gemini AI Agent")
st.info("💡 **Tip:** Use the manual override controls in the sidebar anytime to teach the AI your preferences!")
st.markdown("---")

# Sidebar controls
st.sidebar.header("🎛️ Simulation Control")

# Load resources
model = load_model()
env = load_environment()

# Initialize environment if needed
if st.session_state.current_obs is None and env is not None:
    obs = env.reset()
    if isinstance(obs, tuple):
        obs = obs[0]
    st.session_state.current_obs = np.asarray(obs).flatten()

# Simulation controls
col_start, col_stop, col_reset = st.sidebar.columns(3)

with col_start:
    if st.button("▶️ Start", use_container_width=True):
        st.session_state.simulation_running = True

with col_stop:
    if st.button("⏸️ Pause", use_container_width=True):
        st.session_state.simulation_running = False

with col_reset:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.step_count = 0
        st.session_state.total_reward = 0
        st.session_state.history = {
            'temperature': [],
            'humidity': [],
            'energy': [],
            'actions': [],
            'rewards': [],
            'timestamps': [],
            'comfort': [],
            'lighting': []
        }
        if env:
            obs = env.reset()
            if isinstance(obs, tuple):
                obs = obs[0]
            st.session_state.current_obs = np.asarray(obs).flatten()
        st.session_state.ai_analysis = None

st.sidebar.markdown("---")

# Manual Override Controls - Always visible, no need to enable
st.sidebar.subheader("🎮 Manual Override Controls")
st.sidebar.info("👆 Click to override AI anytime during simulation")

def execute_manual_action(action_id, action_emoji):
    """Execute a manual action and update all state + RECORD TO AI MEMORY"""
    if env and st.session_state.current_obs is not None:
        result = env.step(action_id)
        if len(result) == 4:
            next_obs, reward, done, info = result
        else:
            next_obs, reward, done, truncated, info = result
        if isinstance(next_obs, tuple):
            next_obs = next_obs[0]
        next_obs = np.asarray(next_obs).flatten()
        
        # Update state
        st.session_state.current_obs = next_obs
        st.session_state.last_action = action_id
        st.session_state.last_reward = float(reward)
        st.session_state.total_reward += float(reward)
        st.session_state.step_count += 1
        st.session_state.last_action_source = "Manual"  # Mark as manual override
        
        # Update history
        st.session_state.history['temperature'].append(safe_float(next_obs[0]))
        st.session_state.history['humidity'].append(safe_float(next_obs[1]))
        st.session_state.history['energy'].append(safe_float(next_obs[6]))
        st.session_state.history['comfort'].append(safe_float(next_obs[3]))
        st.session_state.history['lighting'].append(safe_float(next_obs[5]))
        st.session_state.history['actions'].append(action_id)
        st.session_state.history['rewards'].append(float(reward))
        st.session_state.history['timestamps'].append(datetime.now())
        
        # 🧠 RECORD MANUAL OVERRIDE TO AI MEMORY
        if LANGGRAPH_AVAILABLE:
            current_state = {
                "temperature": safe_float(st.session_state.current_obs[0]),
                "humidity": safe_float(st.session_state.current_obs[1]),
                "occupancy": int(safe_float(st.session_state.current_obs[2]) > 5),
                "time_of_day": int(safe_float(st.session_state.current_obs[2])) if safe_float(st.session_state.current_obs[2]) <= 24 else 12,
                "hvac_status": int(safe_float(st.session_state.current_obs[4])),
                "lighting": safe_float(st.session_state.current_obs[5]),
                "energy_usage": safe_float(st.session_state.current_obs[6])
            }
            action_name = ACTION_NAMES.get(action_id, "Unknown")
            add_manual_override(current_state, action_id, action_name)
            st.sidebar.success(f"✅ AI learned from your {action_emoji} action!")
        
        # Force UI update
        st.rerun()

# Manual control buttons - Always visible
manual_col1, manual_col2 = st.sidebar.columns(2)

with manual_col1:
    if st.button("⏭️ Do Nothing", use_container_width=True, key="manual_0"):
        execute_manual_action(0, "⏭️")
    
    if st.button("❄️ HVAC On", use_container_width=True, key="manual_1"):
        execute_manual_action(1, "❄️")
    
    if st.button("💡 Light +", use_container_width=True, key="manual_3"):
        execute_manual_action(3, "💡")

with manual_col2:
    if st.button("🔥 HVAC Off", use_container_width=True, key="manual_2"):
        execute_manual_action(2, "🔥")
    
    if st.button("🌙 Light -", use_container_width=True, key="manual_4"):
        execute_manual_action(4, "🌙")

st.sidebar.markdown("---")

# Simulation speed
speed = st.sidebar.slider("⚡ Simulation Speed (steps/sec)", 0.1, 5.0, 1.0, 0.1)
st.sidebar.markdown("---")

# AI Analysis frequency
ai_freq = st.sidebar.number_input("🧠 AI Analysis Every N Steps", 1, 50, 10)
auto_ai = st.sidebar.checkbox("🤖 Auto AI Analysis", value=True)

st.sidebar.markdown("---")
st.sidebar.metric("📊 Steps", st.session_state.step_count)
st.sidebar.metric("🎯 Total Reward", f"{st.session_state.total_reward:.2f}")

# AI Memory Stats
if LANGGRAPH_AVAILABLE:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 AI Learning Status")
    memory_stats = get_memory_stats()
    st.sidebar.metric("📚 Learning From", f"{memory_stats['total_overrides']} overrides")
    if memory_stats['total_overrides'] > 0:
        st.sidebar.info(f"**Most Common:** {memory_stats['most_common_action']}")
        st.sidebar.success(f"✨ {memory_stats['learning_status']}")
        
        # Show confident patterns
        if memory_stats.get('patterns'):
            with st.sidebar.expander("🎯 Learned Patterns", expanded=True):
                for pattern in memory_stats['patterns'][:3]:  # Show top 3
                    confidence = pattern['confidence']
                    emoji = "🔥" if confidence >= 100 else "⭐" if confidence >= 66 else "💫"
                    
                    st.markdown(f"""
                    **{emoji} {pattern['action_name']}**  
                    📍 {pattern['condition']}  
                    ✅ {pattern['occurrences']} times ({confidence:.0f}% confidence)
                    """)
                    
                    if confidence >= 100:
                        st.success(f"🤖 {pattern['recommendation']}")
    else:
        st.sidebar.info("👉 Use manual controls to teach the AI your preferences!")

# Show environment context if available
if env:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🌍 Environment Info")
    st.sidebar.info(f"**Outside Temp:** {env.outside_temp:.1f}°C")
    st.sidebar.info(f"**Time of Day:** {int(env.time_of_day):02d}:00")
    st.sidebar.info(f"**Current Step:** {env.steps}")
    
    # Target ranges
    with st.sidebar.expander("🎯 Target Ranges"):
        st.write(f"**Temperature:** {env.target_temp_range[0]}-{env.target_temp_range[1]}°C")
        st.write(f"**Lighting:** {env.target_light_range[0]}-{env.target_light_range[1]}%")

# Status indicator
if st.session_state.simulation_running:
    st.sidebar.markdown('<p class="live-indicator" style="color: red; font-size: 20px;">🔴 LIVE</p>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<p style="color: gray; font-size: 20px;">⏸️ PAUSED</p>', unsafe_allow_html=True)

# Main dashboard
if st.session_state.current_obs is not None:
    obs = st.session_state.current_obs
    
    # Top metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        temp = safe_float(obs[0])
        st.metric("🌡️ Temperature", f"{temp:.1f}°C", 
                 delta=f"{temp-22:.1f}°C")
    
    with col2:
        humidity = safe_float(obs[1])
        st.metric("💧 Humidity", f"{humidity:.0f}%")
    
    with col3:
        time_of_day = int(safe_float(obs[2])) if safe_float(obs[2]) <= 24 else 12
        st.metric("� Time", f"{time_of_day:02d}:00")
    
    with col4:
        energy = safe_float(obs[6])
        st.metric("⚡ Energy", f"{energy:.2f} kWh")
    
    with col5:
        comfort = safe_float(obs[3])
        st.metric("😊 Comfort", f"{comfort:.2f}")
    
    # Second row for lighting details
    col_light1, col_light2, col_light3, col_light4 = st.columns(4)
    
    with col_light1:
        lighting = safe_float(obs[5])
        st.metric("💡 Artificial Light", f"{lighting:.0f}%")
    
    with col_light2:
        # Calculate ambient light estimate (0-100 lux range for indoor)
        # Simulate based on time of day
        hour = time_of_day
        if 6 <= hour < 18:  # Daytime
            ambient_lux = np.random.uniform(50, 100)
        elif 18 <= hour < 20:  # Evening
            ambient_lux = np.random.uniform(10, 40)
        else:  # Night
            ambient_lux = np.random.uniform(0, 10)
        st.metric("🌅 Ambient Light", f"{ambient_lux:.0f} lux")
    
    with col_light3:
        # Show ideal lighting for current time
        if 22 <= hour or hour < 6:  # Night
            ideal_range = "0-30%"
            time_period = "🌙 Night"
        elif 6 <= hour < 9:  # Morning
            ideal_range = "40-70%"
            time_period = "🌅 Morning"
        else:  # Day/Evening
            ideal_range = "60-90%"
            time_period = "☀️ Day"
        st.metric(f"{time_period}", f"Ideal: {ideal_range}")
    
    with col_light4:
        occupancy = int(safe_float(obs[2]) > 5)
        st.metric("👥 Occupancy", "🏠 Present" if occupancy else "🚪 Away")
    
    st.markdown("---")
    
    # Main content area
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        # Real-time charts
        st.subheader("📈 Live Environment Monitoring")
        
        if len(st.session_state.history['temperature']) > 0:
            # Create subplot with temperature and energy
            fig = go.Figure()
            
            # Temperature trace
            fig.add_trace(go.Scatter(
                x=list(range(len(st.session_state.history['temperature']))),
                y=st.session_state.history['temperature'],
                name='Temperature',
                line=dict(color='red', width=2),
                yaxis='y'
            ))
            
            # Comfort trace
            fig.add_trace(go.Scatter(
                x=list(range(len(st.session_state.history['comfort']))),
                y=st.session_state.history['comfort'],
                name='Comfort',
                line=dict(color='green', width=2),
                yaxis='y2'
            ))
            
            fig.update_layout(
                title='Temperature & Comfort Over Time',
                xaxis_title='Step',
                yaxis=dict(title='Temperature (°C)', side='left'),
                yaxis2=dict(title='Comfort Score', overlaying='y', side='right'),
                height=300,
                showlegend=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Lighting levels chart
            fig_lighting = go.Figure()
            fig_lighting.add_trace(go.Scatter(
                x=list(range(len(st.session_state.history['lighting']))),
                y=st.session_state.history['lighting'],
                fill='tozeroy',
                name='Lighting',
                line=dict(color='gold', width=2)
            ))
            
            fig_lighting.update_layout(
                title='💡 Lighting Level Over Time',
                xaxis_title='Step',
                yaxis_title='Lighting (%)',
                height=250,
                yaxis=dict(range=[0, 100])
            )
            
            st.plotly_chart(fig_lighting, use_container_width=True)
            
            # Energy consumption
            fig_energy = go.Figure()
            fig_energy.add_trace(go.Scatter(
                x=list(range(len(st.session_state.history['energy']))),
                y=st.session_state.history['energy'],
                fill='tozeroy',
                name='Energy',
                line=dict(color='orange', width=2)
            ))
            
            fig_energy.update_layout(
                title='Energy Consumption',
                xaxis_title='Step',
                yaxis_title='Energy (kWh)',
                height=250
            )
            
            st.plotly_chart(fig_energy, use_container_width=True)
        else:
            st.info("📊 Start simulation to see real-time charts")
        
        # Action history
        st.subheader("🎬 Recent Actions")
        if len(st.session_state.history['actions']) > 0:
            recent_actions = st.session_state.history['actions'][-10:]
            recent_rewards = st.session_state.history['rewards'][-10:]
            
            action_df = pd.DataFrame({
                'Step': range(len(st.session_state.history['actions']) - len(recent_actions), 
                             len(st.session_state.history['actions'])),
                'Action': [ACTION_NAMES.get(a, 'Unknown') for a in recent_actions],
                'Reward': [f"{r:.2f}" for r in recent_rewards]
            })
            st.dataframe(action_df, use_container_width=True, hide_index=True)
    
    with col_right:
        # Current status
        st.subheader("🎛️ Current Status")
        
        hvac_status = bool(safe_float(obs[4]))
        lighting = safe_float(obs[5])
        
        st.info(f"**HVAC:** {'🟢 ON' if hvac_status else '🔴 OFF'}")
        st.info(f"**Lighting:** {lighting:.0f}%")
        
        # Check for auto-apply suggestions based on learned patterns
        if LANGGRAPH_AVAILABLE:
            current_state = {
                "temperature": safe_float(obs[0]),
                "humidity": safe_float(obs[1]),
                "occupancy": int(safe_float(obs[2]) > 5),
                "time_of_day": int(safe_float(obs[2])) if safe_float(obs[2]) <= 24 else 12,
                "hvac_status": int(safe_float(obs[4])),
                "lighting": safe_float(obs[5]),
                "energy_usage": safe_float(obs[6])
            }
            
            auto_suggestion = should_auto_apply(current_state, confidence_threshold=5)
            
            if auto_suggestion.get("should_apply"):
                st.markdown("---")
                st.markdown(f"""
                <div style="padding: 15px; border-radius: 8px; border: 2px solid #9C27B0; 
                            background-color: #f3e5f5; margin: 10px 0px;">
                <h4 style="color: #4a148c; margin-top: 0;">🔮 Pattern Detected!</h4>
                <p style="color:#1a1a1a; font-weight: bold;">{auto_suggestion['action_name']}</p>
                <p style="color:#1a1a1a; font-size: 14px;">
                {auto_suggestion['reason']}<br>
                <strong>Confidence:</strong> {auto_suggestion['confidence']:.0f}%
                </p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Last action with explanation
        action_source = st.session_state.last_action_source
        if action_source == "Manual":
            st.subheader("� Last Action: Manual Override")
        else:
            st.subheader("🤖 Last Action: DQN Model")
            
        if st.session_state.last_action is not None:
            action_name = ACTION_NAMES.get(st.session_state.last_action, 'Unknown')
            
            # Color code based on source
            if action_source == "Manual":
                st.warning(f"**Action:** {action_name} (You overrode)")
            else:
                st.success(f"**Action:** {action_name} (AI decided)")
            
            st.metric("**Reward:**", f"{st.session_state.last_reward:.2f}")
            
            # Show DQN decision explanation
            explanation = explain_dqn_decision(
                obs,  # full observation array
                st.session_state.last_action,
                st.session_state.last_reward
            )
            
            box_color = "#fff8f0" if action_source == "Manual" else "#f0f8f0"
            border_color = "#ff9800" if action_source == "Manual" else "#4CAF50"
            
            st.markdown(f"""
            <div style="padding: 20px; border-radius: 10px; border: 2px solid {border_color}; 
                        background-color: {box_color}; margin: 10px 0px; color: #1a1a1a;">
            <h4 style="margin-top: 0;">💭 Decision Reasoning</h4>
            <p style="color:#1a1a1a;">{explanation}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Ideal conditions for current time
        st.subheader("⭐ Ideal Conditions")
        ideal = get_ideal_conditions(int(safe_float(obs[2])) if safe_float(obs[2]) <= 24 else 12)
        
        st.markdown(f"""
        <div class="agent-box">
        <h4>🕒 {ideal['activity']}</h4>
        <p style="color:#1a1a1a;">
        🌡️ <strong>Temperature:</strong> {ideal['temp_range']}<br>
        💡 <strong>Lighting:</strong> {ideal['light_range']}<br>
        ⚡ <strong>Priority:</strong> {ideal['priority']}
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Manual AI analysis button
        if st.button("🧠 Get AI Analysis Now", use_container_width=True):
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
                    
                    st.session_state.ai_analysis = get_ai_recommendation(current_state)
    
    # AI Analysis Display
    if st.session_state.ai_analysis:
        st.markdown("---")
        st.subheader("🧠 Gemini AI Agent Analysis")
        
        col_rec, col_reason = st.columns(2)
        
        with col_rec:
            st.markdown(f"""
            <div class="agent-box">
            <h4>💡 Recommendation</h4>
            <p style="font-size:18px; font-weight:bold;">{st.session_state.ai_analysis['recommendation']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col_reason:
            st.markdown(f"""
            <div class="ai-box">
            <h4>🧠 Reasoning</h4>
            <p>{st.session_state.ai_analysis['reasoning']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.session_state.ai_analysis.get('analysis'):
            st.markdown(f"""
            <div class="highlight-box">
            <h4>📊 Detailed Analysis</h4>
            <p>{st.session_state.ai_analysis['analysis']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show memory stats if available
        if st.session_state.ai_analysis.get('memory_count', 0) > 0:
            col_mem1, col_mem2 = st.columns(2)
            with col_mem1:
                st.info(f"🧠 **Total Memories:** {st.session_state.ai_analysis['memory_count']}")
            with col_mem2:
                st.info(f"🎯 **Relevant Now:** {st.session_state.ai_analysis.get('relevant_overrides', 0)}")

else:
    st.warning("⚠️ Environment not initialized. Click Reset to start.")

# Simulation loop
if st.session_state.simulation_running and model and env and st.session_state.current_obs is not None:
    placeholder = st.empty()
    
    # Run one step
    obs = st.session_state.current_obs
    
    # Get action from model
    action, _ = model.predict(obs, deterministic=True)
    
    # Take step in environment
    result = env.step(action)
    if len(result) == 4:
        next_obs, reward, done, info = result
    else:
        next_obs, reward, done, truncated, info = result
    
    if isinstance(next_obs, tuple):
        next_obs = next_obs[0]
    next_obs = np.asarray(next_obs).flatten()
    
    # Update state
    st.session_state.current_obs = next_obs
    st.session_state.last_action = int(action)
    st.session_state.last_reward = float(reward)
    st.session_state.total_reward += float(reward)
    st.session_state.step_count += 1
    st.session_state.last_action_source = "DQN"  # Mark as DQN decision
    
    # Update history
    st.session_state.history['temperature'].append(safe_float(next_obs[0]))
    st.session_state.history['humidity'].append(safe_float(next_obs[1]))
    st.session_state.history['energy'].append(safe_float(next_obs[6]))
    st.session_state.history['comfort'].append(safe_float(next_obs[3]))
    st.session_state.history['lighting'].append(safe_float(next_obs[5]))
    st.session_state.history['actions'].append(int(action))
    st.session_state.history['rewards'].append(float(reward))
    st.session_state.history['timestamps'].append(datetime.now())
    
    # Auto AI analysis
    if auto_ai and LANGGRAPH_AVAILABLE and st.session_state.step_count % ai_freq == 0:
        current_state = {
            "temperature": safe_float(next_obs[0]),
            "humidity": safe_float(next_obs[1]),
            "occupancy": int(safe_float(next_obs[2]) > 5),
            "time_of_day": int(safe_float(next_obs[2])) if safe_float(next_obs[2]) <= 24 else 12,
            "hvac_status": int(safe_float(next_obs[4])),
            "lighting": safe_float(next_obs[5]),
            "energy_usage": safe_float(next_obs[6])
        }
        st.session_state.ai_analysis = get_ai_recommendation(current_state)
    
    # Reset if done
    if done:
        obs = env.reset()
        if isinstance(obs, tuple):
            obs = obs[0]
        st.session_state.current_obs = np.asarray(obs).flatten()
    
    # Sleep based on speed
    time.sleep(1.0 / speed)
    
    # Trigger rerun
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🤖 <b>Smart Home AI - Live Simulation</b> | Real-Time DQN + Gemini AI Integration</p>
    <p>Built with Streamlit, Stable-Baselines3, LangGraph & Google Gemini</p>
</div>
""", unsafe_allow_html=True)
