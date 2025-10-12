import streamlit as st
import pandas as pd
import numpy as np
from stable_baselines3 import DQN
from environment import SmartHomeEnv
import plotly.graph_objects as go
import plotly.express as px
import time
import random

st.set_page_config(page_title="Smart Home AI Dashboard", layout="wide", page_icon="🏠")

# Custom CSS for better styling
st.markdown("""
<style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
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
</style>
""", unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    try:
        return DQN.load("smart_home_ai_brain.zip")
    except Exception as e:
        st.error(f"❌ Could not load model: {e}")
        st.info("💡 Please train the model first by running: `python train.py`")
        st.stop()

# Load environment
@st.cache_resource
def load_environment():
    try:
        return SmartHomeEnv(data_file="SmartHome_Realistic_Dataset.csv")
    except FileNotFoundError:
        st.error("❌ Could not load environment: Dataset file not found")
        st.warning("📁 Looking for: `SmartHome_Realistic_Dataset.csv`")
        st.info("💡 Please generate the dataset first by running:")
        st.code("python generate_realistic_dataset.py", language="bash")
        st.stop()
    except Exception as e:
        st.error(f"❌ Could not load environment: {e}")
        st.stop()

def explain_ai_decision(obs, action, reward):
    """Explain why the AI chose this action"""
    temp = obs[0]
    light = obs[2]
    comfort = obs[3]
    fan_on = bool(obs[4])
    light_percent = obs[5]
    energy = obs[6]
    
    explanations = []
    
    # Temperature reasoning
    if action == 1:  # Turn fan ON
        explanations.append(f"🌡️ **Temperature is {temp:.1f}°C** (warm), turning fan ON to cool the room")
        if temp > 26:
            explanations.append("   → Room is getting uncomfortable, cooling is needed")
    elif action == 2:  # Turn fan OFF
        explanations.append(f"🌡️ **Temperature is {temp:.1f}°C** (comfortable), turning fan OFF to save energy")
        if temp < 24:
            explanations.append("   → Room is cool enough, no need for cooling")
    
    # Light reasoning
    if action == 3:  # Increase light
        explanations.append(f"💡 **Light is {light:.0f} lux** (dim), increasing brightness for better comfort")
        if light < 200:
            explanations.append("   → Room is too dark for activities")
    elif action == 4:  # Decrease light
        explanations.append(f"💡 **Light is {light:.0f} lux** (bright), decreasing to save energy")
        if light > 800:
            explanations.append("   → Room has sufficient natural/artificial light")
    
    # Do nothing reasoning
    if action == 0:
        explanations.append(f"✅ **Conditions are optimal** - no changes needed")
        explanations.append(f"   → Temperature: {temp:.1f}°C (ideal: 22-25°C)")
        explanations.append(f"   → Light: {light:.0f} lux (adequate)")
        explanations.append(f"   → Comfort: {comfort:.2f} (good)")
    
    # Reward explanation
    if reward > 5:
        explanations.append(f"🎉 **High reward (+{reward:.1f})**: Great decision! High comfort with low energy")
    elif reward > 0:
        explanations.append(f"✅ **Positive reward (+{reward:.1f})**: Good balance of comfort and efficiency")
    elif reward > -5:
        explanations.append(f"⚠️ **Small penalty ({reward:.1f})**: Minor inefficiency or discomfort")
    else:
        explanations.append(f"❌ **Large penalty ({reward:.1f})**: Poor comfort or high energy waste")
    
    return explanations

def get_ideal_conditions(current_hour):
    """Get ideal conditions based on time of day"""
    if 22 <= current_hour or current_hour < 6:  # Night/Sleep
        return {
            'temp_range': (20, 23),
            'light_range': (0, 100),
            'activity': 'Sleeping',
            'priority': 'Low energy, darker environment'
        }
    elif 6 <= current_hour < 9:  # Morning
        return {
            'temp_range': (21, 24),
            'light_range': (300, 600),
            'activity': 'Waking up',
            'priority': 'Moderate lighting, comfortable temperature'
        }
    elif 9 <= current_hour < 17:  # Day
        return {
            'temp_range': (22, 25),
            'light_range': (400, 800),
            'activity': 'Working/Active',
            'priority': 'Good lighting, comfortable temperature'
        }
    else:  # Evening (17-22)
        return {
            'temp_range': (21, 24),
            'light_range': (200, 500),
            'activity': 'Relaxing',
            'priority': 'Moderate lighting, comfort focus'
        }

# Header
st.title("🏠 Smart Home AI Control Dashboard")
st.markdown("**Watch your AI make intelligent decisions to balance comfort and energy efficiency**")

# Load resources
model = load_model()
env = load_environment()

# Sidebar controls
st.sidebar.header("⚙️ Simulation Controls")

# TIME OF DAY SELECTOR
time_options = {
    "6:00 AM - Morning": 360,
    "9:00 AM - Work Start": 540,
    "12:00 PM - Lunch": 720,
    "3:00 PM - Afternoon": 900,
    "6:00 PM - Evening": 1080,
    "9:00 PM - Night": 1260,
    "Random Time": -1
}

selected_time = st.sidebar.selectbox("🕐 Start Time of Day", list(time_options.keys()))
start_step = time_options[selected_time]

if start_step == -1:
    start_step = random.randint(360, 1380)

auto_run = st.sidebar.checkbox("▶️ Auto-run simulation", value=False)
speed = st.sidebar.slider("⏱️ Simulation speed (seconds)", 0.1, 2.0, 1.0)

# Store auto_run in session state to trigger automatic execution
if 'auto_run_enabled' not in st.session_state:
    st.session_state.auto_run_enabled = auto_run
elif st.session_state.auto_run_enabled != auto_run:
    st.session_state.auto_run_enabled = auto_run
    if auto_run:
        st.rerun()  # Immediately trigger when auto-run is enabled

# SCENARIO SELECTOR
st.sidebar.markdown("### 🎭 Scenario")
scenarios = {
    "Normal Day": {"desc": "Regular conditions", "temp_offset": 0},
    "Hot Summer Day": {"desc": "Very warm weather", "temp_offset": 12},
    "Cold Winter Day": {"desc": "Chilly weather", "temp_offset": -4},
    "Heat Wave": {"desc": "Extremely hot", "temp_offset": 18}
}

selected_scenario = st.sidebar.selectbox("Choose scenario", list(scenarios.keys()))
st.sidebar.info(scenarios[selected_scenario]["desc"])

# Detect scenario or time change and auto-restart
if 'last_scenario' not in st.session_state:
    st.session_state.last_scenario = selected_scenario
    st.session_state.last_time = selected_time
elif st.session_state.last_scenario != selected_scenario or st.session_state.last_time != selected_time:
    st.session_state.last_scenario = selected_scenario
    st.session_state.last_time = selected_time
    st.session_state.initialized = False  # Force restart
    st.info("🔄 Settings changed - restarting simulation...")

# Initialize session state
if 'initialized' not in st.session_state or not st.session_state.initialized or st.sidebar.button("🔄 Restart Simulation"):
    st.session_state.initialized = True
    st.session_state.history = []
    st.session_state.total_reward = 0
    
    # Reset environment to start step
    obs, _ = env.reset()
    env.current_step = min(start_step, len(env.df) - 1)
    st.session_state.obs = env._get_obs()
    st.session_state.step = env.current_step

if 'obs' not in st.session_state:
    st.session_state.obs, _ = env.reset()
    st.session_state.step = 0
    st.session_state.history = []
    st.session_state.total_reward = 0

# Apply scenario temperature offset to ACTUAL observation
temp_offset = scenarios[selected_scenario]["temp_offset"]
# Modify the actual observation for both display and AI
display_obs = st.session_state.obs.copy()
display_obs[0] = float(st.session_state.obs[0] + temp_offset)

# Calculate current time
current_hour = (st.session_state.step // 60) % 24
current_minute = st.session_state.step % 60
ideal_conditions = get_ideal_conditions(current_hour)

# Show current time and context
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown(f"### 🕐 {current_hour:02d}:{current_minute:02d}")
    st.caption(f"**{ideal_conditions['activity']}** time")
with col2:
    st.markdown(f"### 📍 Current Context")
    st.caption(f"**Scenario:** {selected_scenario}")
    st.caption(f"**Priority:** {ideal_conditions['priority']}")

# Main dashboard
st.markdown("---")
st.markdown("## 📊 Current Environment Status")

col1, col2, col3, col4 = st.columns(4)

# Temperature
with col1:
    temp = display_obs[0]
    ideal_temp = ideal_conditions['temp_range']
    
    if ideal_temp[0] <= temp <= ideal_temp[1]:
        temp_status = "✅ Ideal"
        temp_color = "normal"
    elif temp > ideal_temp[1]:
        temp_status = "🔥 Too Hot"
        temp_color = "inverse"
    else:
        temp_status = "🥶 Too Cold"
        temp_color = "inverse"
    
    st.metric("🌡️ Temperature", f"{temp:.1f}°C", f"{temp_status}")
    st.caption(f"Ideal: {ideal_temp[0]}-{ideal_temp[1]}°C")

# Light
with col2:
    light = display_obs[2]
    ideal_light = ideal_conditions['light_range']
    
    if ideal_light[0] <= light <= ideal_light[1]:
        light_status = "✅ Good"
    elif light > ideal_light[1]:
        light_status = "☀️ Too Bright"
    else:
        light_status = "🌙 Too Dim"
    
    st.metric("💡 Light Level", f"{light:.0f} lux", light_status)
    st.caption(f"Ideal: {ideal_light[0]}-{ideal_light[1]} lux")

# Comfort
with col3:
    comfort = display_obs[3]
    if comfort > 0.7:
        comfort_status = "😊 Great"
    elif comfort > 0.5:
        comfort_status = "😐 OK"
    else:
        comfort_status = "😟 Poor"
    
    st.metric("😊 Comfort Score", f"{comfort:.2f}", comfort_status)
    
    # Comfort bar
    st.progress(float(comfort))

# Energy
with col4:
    energy = display_obs[6]
    if energy < 1.5:
        energy_status = "💚 Efficient"
    elif energy < 2.5:
        energy_status = "🔋 Normal"
    else:
        energy_status = "⚡ High"
    
    st.metric("⚡ Energy", f"{energy:.2f} kW", energy_status)
    st.caption(f"Total: {st.session_state.total_reward:.1f}")

# Device Status
st.markdown("### 🔧 Device Status")
col1, col2 = st.columns(2)
with col1:
    fan_on = bool(display_obs[4])
    if fan_on:
        st.success("🌀 **Fan:** ON (Cooling)")
    else:
        st.info("⏹️ **Fan:** OFF")

with col2:
    light_percent = display_obs[5]
    if light_percent > 70:
        st.success(f"🔆 **Lights:** {light_percent:.0f}% (Bright)")
    elif light_percent > 30:
        st.info(f"💡 **Lights:** {light_percent:.0f}% (Medium)")
    else:
        st.warning(f"🔅 **Lights:** {light_percent:.0f}% (Dim)")

# Control Actions
st.markdown("---")
st.markdown("## 🎮 Control Panel")
st.caption("Let the AI decide automatically, or take manual control")

col1, col2, col3, col4, col5 = st.columns(5)

action_taken = None
with col1:
    if st.button("⏸️ Do Nothing", use_container_width=True):
        action_taken = 0
with col2:
    if st.button("🌀 Fan ON", use_container_width=True):
        action_taken = 1
with col3:
    if st.button("⏹️ Fan OFF", use_container_width=True):
        action_taken = 2
with col4:
    if st.button("🔆 Light +20%", use_container_width=True):
        action_taken = 3
with col5:
    if st.button("🔅 Light -20%", use_container_width=True):
        action_taken = 4

# AI Decision or Manual Override
if auto_run or action_taken is not None:
    if action_taken is None:
        # Let AI decide
        action, _ = model.predict(display_obs, deterministic=True)
        action = int(action)
        decision_maker = "🤖 AI"
    else:
        action = action_taken
        decision_maker = "👤 You"
    
    # Execute action (use original obs without temp offset for actual env)
    new_obs, reward, terminated, _, _ = env.step(action)
    
    st.session_state.total_reward += reward
    
    # Get AI explanation
    explanations = explain_ai_decision(display_obs, action, reward)
    
    # Store history
    st.session_state.history.append({
        'step': st.session_state.step,
        'time': f"{current_hour:02d}:{current_minute:02d}",
        'temperature': display_obs[0],
        'light': display_obs[2],
        'comfort': display_obs[3],
        'energy': display_obs[6],
        'action': action,
        'reward': reward,
        'decision_maker': decision_maker
    })
    
    st.session_state.obs = new_obs
    st.session_state.step += 1
    
    # Show decision with explanation
    action_names = ["⏸️ Do Nothing", "🌀 Turn Fan ON", "⏹️ Turn Fan OFF", "🔆 Increase Light", "🔅 Decrease Light"]
    
    st.markdown("---")
    st.markdown("## 🧠 AI Decision Explanation")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if reward > 0:
            st.success(f"### {decision_maker} Action")
        else:
            st.warning(f"### {decision_maker} Action")
        
        st.markdown(f"**{action_names[action]}**")
        st.metric("Reward", f"{reward:.2f}", delta=f"{reward:.2f}")
    
    with col2:
        st.markdown("### 💭 Why this decision?")
        for explanation in explanations:
            st.markdown(explanation)
    
    if terminated:
        st.warning("🏁 Simulation completed! Click 'Restart Simulation' to continue.")
    
    if auto_run:
        time.sleep(speed)
        st.rerun()

# Performance History
if st.session_state.history:
    st.markdown("---")
    st.markdown("## 📈 Performance Analytics")
    
    df_history = pd.DataFrame(st.session_state.history)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_reward = df_history['reward'].sum()
        st.metric("💰 Total Reward", f"{total_reward:.1f}")
    with col2:
        avg_comfort = df_history['comfort'].mean()
        st.metric("😊 Avg Comfort", f"{avg_comfort:.2f}")
    with col3:
        avg_energy = df_history['energy'].mean()
        st.metric("⚡ Avg Energy", f"{avg_energy:.2f} kW")
    with col4:
        ai_decisions = len(df_history[df_history['decision_maker'] == '🤖 AI'])
        st.metric("🤖 AI Decisions", f"{ai_decisions}/{len(df_history)}")
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["🏠 Environment Trends", "🎯 Action Analysis", "💡 Insights"])
    
    with tab1:
        st.markdown("### 📊 What You're Seeing:")
        st.markdown("""
        **This chart shows how room conditions change over time as the AI controls devices.**
        
        - 🔴 **Red Line (Temperature):** Shows room temperature in °C. Watch how it responds when the AI turns the fan on/off.
        - 🟢 **Green Line (Comfort ×30):** User comfort score scaled up for visibility. Higher = more comfortable.
        
        **Look for:**
        - 📉 Temperature **drops** when fan turns ON (AI cooling the room)
        - 📈 Temperature **rises** when fan turns OFF (AI saving energy)
        - 🎯 Comfort **increases** when conditions improve (good lighting + comfortable temp)
        - ⚖️ AI balancing: Not always perfect temp, but good enough to save energy
        """)
        
        # Environment over time
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_history['time'], y=df_history['temperature'],
            name='Temperature (°C)', line=dict(color='red', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=df_history['time'], y=df_history['comfort']*30,
            name='Comfort (×30)', line=dict(color='green', width=2)
        ))
        fig.update_layout(
            title="Environment Conditions Over Time",
            xaxis_title="Time",
            yaxis_title="Value",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 🎮 Understanding AI Actions:")
        st.markdown("""
        **The AI can take 5 different actions to control your smart home:**
        
        1. ⏸️ **Do Nothing** - Room is already comfortable, no changes needed (saves energy!)
        2. 🌀 **Fan ON** - Room is too hot, activate cooling
        3. ⏹️ **Fan OFF** - Room is cool enough, turn off to save energy
        4. 🔆 **Light +20%** - Room is too dark, increase brightness for activities
        5. 🔅 **Light -20%** - Room is bright enough or too bright, dim lights to save energy
        
        **What's Smart About It:**
        - AI doesn't just react blindly - it considers **time of day**, **current conditions**, and **energy cost**
        - A high "Do Nothing" count means the AI is **maintaining good conditions efficiently**
        - Actions should vary based on the scenario you selected (Hot Day = more cooling)
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Action distribution
            action_names_dict = {
                0: "⏸️ Do Nothing",
                1: "🌀 Fan ON",
                2: "⏹️ Fan OFF",
                3: "🔆 Light Up",
                4: "🔅 Light Down"
            }
            df_history['action_name'] = df_history['action'].map(action_names_dict)
            action_counts = df_history['action_name'].value_counts()
            
            fig = px.pie(
                values=action_counts.values,
                names=action_counts.index,
                title="Action Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Reward over time
            fig = px.line(
                df_history, x='time', y='reward',
                title="Reward Per Step",
                color_discrete_sequence=['purple']
            )
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 💡 Performance Insights & Understanding Your AI")
        
        # Add learning explanation box at the top
        st.markdown("""
        <div class="highlight-box">
        <h4>🧠 How Your AI Learns (Important!)</h4>
        <p><strong>Current Mode: OFFLINE TRAINING</strong></p>
        <ul>
        <li>✅ The AI <strong>already learned</strong> from 30 days of data (43,200 samples)</li>
        <li>✅ It learned patterns like: "26°C + Fan ON → Comfort UP, Energy Cost ACCEPTABLE"</li>
        <li>❌ It does <strong>NOT learn in real-time</strong> from your manual interventions right now</li>
        <li>❌ If you turn off the fan when temp is 26°C, the AI won't update its behavior immediately</li>
        </ul>
        <p><strong>Why?</strong> This is a <strong>pre-trained model</strong> - like a student who studied and graduated. 
        It doesn't go back to school every time you correct it.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Analysis
        if total_reward > 0:
            st.success("✅ **Overall Performance:** Excellent! The AI is successfully balancing comfort and energy efficiency.")
        else:
            st.warning("⚠️ **Overall Performance:** Needs improvement. The AI should focus more on user comfort.")
        
        # Comfort analysis
        if avg_comfort > 0.7:
            st.info("😊 **Comfort Level:** Users are very comfortable most of the time.")
            st.caption("   → AI is prioritizing comfort effectively. Most decisions result in pleasant conditions.")
        elif avg_comfort > 0.5:
            st.warning("😐 **Comfort Level:** Moderate comfort. Room conditions could be better.")
            st.caption("   → AI is being too conservative with energy. Users deserve better conditions.")
        else:
            st.error("😟 **Comfort Level:** Poor comfort. Immediate adjustments needed.")
            st.caption("   → AI needs retraining with updated priorities. User comfort is suffering.")
        
        # Energy analysis
        if avg_energy < 1.5:
            st.success("💚 **Energy Efficiency:** Excellent! Very low energy consumption.")
            st.caption("   → AI is keeping costs low while maintaining comfort. Great balance!")
        elif avg_energy < 2.5:
            st.info("🔋 **Energy Efficiency:** Good balance of comfort and energy use.")
            st.caption("   → AI uses energy when needed for comfort, but doesn't waste it.")
        else:
            st.warning("⚡ **Energy Efficiency:** High energy consumption. Consider energy-saving measures.")
            st.caption("   → AI might be over-correcting or devices are running unnecessarily.")
        
        # Action insights
        most_common_action = df_history['action_name'].mode()[0]
        st.info(f"🎯 **Most Common Action:** {most_common_action}")
        
        if "Do Nothing" in most_common_action:
            st.success("✅ The AI maintains optimal conditions effectively!")
            st.caption("   → High 'Do Nothing' count = Room stays comfortable without constant adjustments")
        else:
            st.info("🔧 The AI actively adjusts conditions to maintain comfort.")
            st.caption("   → AI is responding to changing conditions (time of day, temperature, occupancy)")
        
        st.markdown("---")
        
        # Future feature teaser
        st.markdown("""
        <div class="warning-box">
        <h4>🚀 Want Real-Time Learning? (Future Feature)</h4>
        <p>To make the AI learn from YOUR manual corrections, we'd need to implement:</p>
        <ul>
        <li>🔄 <strong>Online Learning</strong>: AI updates its model after each interaction</li>
        <li>💾 <strong>User Preference Memory</strong>: Store your manual overrides as training data</li>
        <li>🎯 <strong>Personalized Profiles</strong>: "User prefers cooler temps in the evening"</li>
        <li>📊 <strong>A/B Testing</strong>: Compare AI decisions vs your preferences to improve</li>
        </ul>
        <p><strong>Example:</strong> You turn fan OFF at 26°C → AI learns "this user tolerates warmer temps" 
        → Next time at 26°C, AI is less aggressive with cooling.</p>
        <p><em>This would require significant architecture changes (reinforcement learning with human feedback).</em></p>
        </div>
        """, unsafe_allow_html=True)

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 How to Use")
st.sidebar.markdown("""
1. **Select a time** to start simulation
2. **Choose a scenario** to test AI
3. **Enable auto-run** to watch AI work
4. **Or use manual controls** to test yourself
5. **Watch the explanations** to understand AI decisions
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 AI Goals")
st.sidebar.markdown("""
The AI tries to:
- ✅ **Maximize comfort** (ideal temp + lighting)
- 💰 **Minimize energy** (turn off when possible)
- ⚖️ **Balance both** (comfort worth energy cost?)
- 🧠 **Learn patterns** (from 30 days of data)

**Decision Formula:**
```
Reward = 
  Comfort×10      [0-10 points]
  - Energy×2      [penalty]
  - Override×20   [big penalty]
  - Action×0.5    [tiny penalty]
```
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### ❓ Common Questions")
st.sidebar.markdown("""
**Q: Why does AI keep fan OFF at 26°C?**
A: It learned that 26°C is acceptable for most users, and saving energy is important.

**Q: Can I teach it my preferences?**
A: Not yet! The AI uses pre-trained knowledge. Real-time learning is a future feature.

**Q: What if I disagree with AI?**
A: Use manual controls to test your own strategy and compare rewards!

**Q: Why "Do Nothing" so much?**
A: That's actually good! It means conditions are already optimal.
""")
