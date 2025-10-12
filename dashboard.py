import streamlit as st
import pandas as pd
import numpy as np
from stable_baselines3 import DQN
from environment import SmartHomeEnv
import plotly.graph_objects as go
import plotly.express as px
import time

st.set_page_config(page_title="Smart Home AI Dashboard", layout="wide")

# Load the trained model
@st.cache_resource
def load_model():
    return DQN.load("smart_home_ai_brain.zip")

# Load environment
@st.cache_resource
def load_environment():
    return SmartHomeEnv(data_file="SmartHome_Realistic_Dataset.csv")

st.title("🏠 Smart Home AI Control Dashboard")

model = load_model()
env = load_environment()

# Sidebar controls
st.sidebar.header("Simulation Controls")
auto_run = st.sidebar.checkbox("Auto-run simulation")
speed = st.sidebar.slider("Simulation speed (seconds)", 0.1, 2.0, 0.5)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.obs, _ = env.reset()
    st.session_state.history = []

# Main dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Current Temperature", f"{st.session_state.obs[0]:.1f}°C")
    st.metric("Ambient Light", f"{st.session_state.obs[2]:.0f} lux")

with col2:
    st.metric("Comfort Score", f"{st.session_state.obs[3]:.2f}")
    st.metric("Energy Consumed", f"{st.session_state.obs[6]:.2f} kW")

with col3:
    fan_status = "ON" if st.session_state.obs[4] == 1 else "OFF"
    st.metric("Fan Status", fan_status)
    st.metric("Light Level", f"{st.session_state.obs[5]:.0f}%")

# Action buttons
st.subheader("Manual Override (or watch AI decide)")
col1, col2, col3, col4, col5 = st.columns(5)

action_taken = None
with col1:
    if st.button("Do Nothing"):
        action_taken = 0
with col2:
    if st.button("Turn Fan ON"):
        action_taken = 1
with col3:
    if st.button("Turn Fan OFF"):
        action_taken = 2
with col4:
    if st.button("Increase Light"):
        action_taken = 3
with col5:
    if st.button("Decrease Light"):
        action_taken = 4

# AI Decision or Manual Override
if auto_run or action_taken is not None:
    if action_taken is None:
        # Let AI decide
        action, _ = model.predict(st.session_state.obs, deterministic=True)
        action = int(action)
        decision_maker = "AI"
    else:
        action = action_taken
        decision_maker = "Manual"
    
    # Execute action
    new_obs, reward, terminated, _, _ = env.step(action)
    
    # Store history
    st.session_state.history.append({
        'step': st.session_state.step,
        'temperature': st.session_state.obs[0],
        'light': st.session_state.obs[2],
        'comfort': st.session_state.obs[3],
        'energy': st.session_state.obs[6],
        'action': action,
        'reward': reward,
        'decision_maker': decision_maker
    })
    
    st.session_state.obs = new_obs
    st.session_state.step += 1
    
    # Show last action
    action_names = ["Do Nothing", "Turn Fan ON", "Turn Fan OFF", "Increase Light", "Decrease Light"]
    st.success(f"Step {st.session_state.step}: {decision_maker} chose '{action_names[action]}' (Reward: {reward:.2f})")
    
    if terminated:
        st.warning("Simulation completed!")
    
    time.sleep(speed)
    st.rerun()

# History charts
if st.session_state.history:
    st.subheader("📊 Performance History")
    
    df_history = pd.DataFrame(st.session_state.history)
    
    # Temperature and comfort over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_history['step'], y=df_history['temperature'], 
                            name='Temperature (°C)', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df_history['step'], y=df_history['comfort']*40, 
                            name='Comfort Score (×40)', line=dict(color='green')))
    fig.update_layout(title="Temperature vs Comfort Over Time")
    st.plotly_chart(fig, use_container_width=True)
    
    # Actions taken
    action_counts = df_history['action'].value_counts()
    fig_actions = px.bar(x=action_counts.index, y=action_counts.values, 
                        title="Actions Taken by AI/Manual")
    st.plotly_chart(fig_actions, use_container_width=True)

# Reset button
if st.sidebar.button("Reset Simulation"):
    st.session_state.step = 0
    st.session_state.obs, _ = env.reset()
    st.session_state.history = []
    st.rerun()