import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from stable_baselines3 import DQN
from environment import SmartHomeEnv
import time
from datetime import datetime

st.set_page_config(page_title="AI Performance Monitor", layout="wide")

class RealTimeValidator:
    def __init__(self):
        self.performance_history = []
        self.benchmarks = {
            'comfort_target': 0.7,
            'energy_limit': 3.0,
            'temp_range': (20, 24),
            'efficiency_target': 0.5  # comfort per energy unit
        }
    
    def calculate_real_time_metrics(self, obs, action, reward, step):
        """Calculate performance metrics for current step"""
        temp, perceived_temp, light, comfort, fan_state, light_pct, energy = obs
        hour = (step // 60) % 24
        
        metrics = {
            'timestamp': datetime.now(),
            'step': step,
            'hour': hour,
            'temperature': temp,
            'comfort': comfort,
            'energy': energy,
            'action': action,
            'reward': reward,
            
            # Performance indicators
            'temp_in_range': 1 if 20 <= temp <= 24 else 0,
            'comfort_good': 1 if comfort >= 0.7 else 0,
            'energy_efficient': 1 if energy <= 3.0 else 0,
            'efficiency_ratio': comfort / (energy + 0.1),
            
            # Context-aware metrics
            'appropriate_action': self._evaluate_action_appropriateness(obs, action),
            'user_satisfaction': self._estimate_user_satisfaction(obs, action)
        }
        
        self.performance_history.append(metrics)
        return metrics
    
    def _evaluate_action_appropriateness(self, obs, action):
        """Evaluate if the action makes sense given the context"""
        temp, _, light, comfort, fan_state, light_pct, energy = obs
        
        # Action appropriateness rules
        if action == 0:  # Do nothing
            return 0.7  # Neutral score
        elif action == 1:  # Turn fan on
            if temp > 23 and fan_state == 0:
                return 1.0  # Good decision
            elif temp < 21:
                return 0.2  # Poor decision
            else:
                return 0.5
        elif action == 2:  # Turn fan off  
            if temp < 21 and fan_state == 1:
                return 1.0  # Good decision
            elif temp > 25:
                return 0.2  # Poor decision
            else:
                return 0.5
        elif action == 3:  # Increase light
            if light < 300 and 6 <= (len(self.performance_history) // 60) % 24 <= 22:
                return 0.9  # Good for daytime
            elif light > 800:
                return 0.3  # May be too bright
            else:
                return 0.6
        elif action == 4:  # Decrease light
            if light > 600 and 22 <= (len(self.performance_history) // 60) % 24 or (len(self.performance_history) // 60) % 24 <= 6:
                return 0.9  # Good for nighttime
            elif light < 200:
                return 0.3  # May be too dark
            else:
                return 0.6
        
        return 0.5  # Default neutral
    
    def _estimate_user_satisfaction(self, obs, action):
        """Estimate user satisfaction based on comfort and energy"""
        temp, _, light, comfort, fan_state, light_pct, energy = obs
        
        # Comfort satisfaction (60% weight)
        comfort_satisfaction = min(1.0, comfort / 0.8)
        
        # Temperature satisfaction (25% weight)  
        temp_satisfaction = 1.0 if 20 <= temp <= 24 else max(0, 1 - abs(temp - 22) / 10)
        
        # Energy satisfaction (15% weight) - lower is better
        energy_satisfaction = max(0, 1 - energy / 5.0)
        
        total_satisfaction = (comfort_satisfaction * 0.6 + 
                            temp_satisfaction * 0.25 + 
                            energy_satisfaction * 0.15)
        
        return min(1.0, total_satisfaction)
    
    def get_performance_summary(self, window_size=50):
        """Get performance summary for recent history"""
        if len(self.performance_history) < window_size:
            recent_data = self.performance_history
        else:
            recent_data = self.performance_history[-window_size:]
        
        if not recent_data:
            return {}
        
        df = pd.DataFrame(recent_data)
        
        summary = {
            'avg_comfort': df['comfort'].mean(),
            'avg_energy': df['energy'].mean(),
            'avg_efficiency': df['efficiency_ratio'].mean(),
            'temp_in_range_pct': df['temp_in_range'].mean() * 100,
            'comfort_good_pct': df['comfort_good'].mean() * 100,
            'energy_efficient_pct': df['energy_efficient'].mean() * 100,
            'avg_user_satisfaction': df['user_satisfaction'].mean(),
            'avg_action_appropriateness': df['appropriate_action'].mean(),
            'total_reward': df['reward'].sum(),
            'recent_steps': len(recent_data)
        }
        
        # Calculate performance grade
        overall_score = (summary['avg_comfort'] * 0.4 + 
                        summary['avg_user_satisfaction'] * 0.3 +
                        summary['avg_action_appropriateness'] * 0.3)
        
        if overall_score >= 0.85:
            summary['grade'] = "A+"
            summary['status'] = "🏆 Excellent"
        elif overall_score >= 0.75:
            summary['grade'] = "A"
            summary['status'] = "🥇 Very Good"
        elif overall_score >= 0.65:
            summary['grade'] = "B"
            summary['status'] = "🥈 Good"
        elif overall_score >= 0.55:
            summary['grade'] = "C"
            summary['status'] = "🥉 Average"
        else:
            summary['grade'] = "F"
            summary['status'] = "❌ Poor"
        
        summary['overall_score'] = overall_score
        return summary

# Streamlit App
st.title("🔍 Smart Home AI Performance Monitor")

# Load model and environment
@st.cache_resource
def load_components():
    try:
        model = DQN.load("smart_home_ai_brain.zip")
        env = SmartHomeEnv(data_file="SmartHome_Realistic_Dataset.csv")
        return model, env
    except Exception as e:
        st.error(f"Error loading components: {e}")
        return None, None

model, env = load_components()

if model is None or env is None:
    st.error("❌ Could not load AI model or environment. Please ensure files exist.")
    st.stop()

# Initialize validator
if 'validator' not in st.session_state:
    st.session_state.validator = RealTimeValidator()
    st.session_state.step_count = 0
    st.session_state.obs, _ = env.reset()

validator = st.session_state.validator

# Sidebar controls
st.sidebar.header("🎛️ Monitoring Controls")
monitoring_enabled = st.sidebar.checkbox("🔄 Enable Real-time Monitoring", value=False)
update_frequency = st.sidebar.slider("Update Frequency (seconds)", 0.5, 5.0, 1.0)

# Performance targets
st.sidebar.header("🎯 Performance Targets")
comfort_target = st.sidebar.slider("Comfort Target", 0.0, 1.0, 0.7)
energy_limit = st.sidebar.slider("Energy Limit (kW)", 0.0, 10.0, 3.0)

validator.benchmarks['comfort_target'] = comfort_target
validator.benchmarks['energy_limit'] = energy_limit

# Main monitoring display
if monitoring_enabled:
    # Take one step
    action, _ = model.predict(st.session_state.obs, deterministic=True)
    action = int(action)
    
    new_obs, reward, terminated, _, _ = env.step(action)
    
    # Calculate metrics
    metrics = validator.calculate_real_time_metrics(
        st.session_state.obs, action, reward, st.session_state.step_count
    )
    
    st.session_state.obs = new_obs
    st.session_state.step_count += 1
    
    # Display current metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp_status = "✅" if metrics['temp_in_range'] else "⚠️"
        st.metric("🌡️ Temperature", f"{metrics['temperature']:.1f}°C", 
                 delta=temp_status)
    
    with col2:
        comfort_status = "✅" if metrics['comfort_good'] else "⚠️"
        st.metric("😊 Comfort", f"{metrics['comfort']:.2f}", 
                 delta=comfort_status)
    
    with col3:
        energy_status = "✅" if metrics['energy_efficient'] else "⚠️"
        st.metric("⚡ Energy", f"{metrics['energy']:.2f} kW", 
                 delta=energy_status)
    
    with col4:
        st.metric("🎮 Action", f"{['⏸️', '🌀+', '🌀-', '💡+', '💡-'][action]}", 
                 delta=f"Score: {metrics['appropriate_action']:.2f}")

# Performance summary
if len(validator.performance_history) > 0:
    summary = validator.get_performance_summary()
    
    st.header("📊 Performance Summary")
    
    # Status overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Grade", summary['grade'], summary['status'])
    
    with col2:
        st.metric("User Satisfaction", f"{summary['avg_user_satisfaction']:.2f}/1.0",
                 f"{summary['avg_user_satisfaction']*100:.1f}%")
    
    with col3:
        st.metric("Action Intelligence", f"{summary['avg_action_appropriateness']:.2f}/1.0",
                 f"{summary['avg_action_appropriateness']*100:.1f}%")
    
    # Detailed metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏠 Comfort & Environment")
        st.write(f"• Average Comfort: **{summary['avg_comfort']:.3f}**/1.0")
        st.write(f"• Temperature in Range: **{summary['temp_in_range_pct']:.1f}%** of time")
        st.write(f"• Good Comfort: **{summary['comfort_good_pct']:.1f}%** of time")
    
    with col2:
        st.subheader("⚡ Energy & Efficiency")
        st.write(f"• Average Energy: **{summary['avg_energy']:.2f}** kW")
        st.write(f"• Efficiency Ratio: **{summary['avg_efficiency']:.2f}**")
        st.write(f"• Energy Efficient: **{summary['energy_efficient_pct']:.1f}%** of time")
    
    # Performance charts
    if len(validator.performance_history) >= 10:
        st.header("📈 Performance Trends")
        
        df_history = pd.DataFrame(validator.performance_history[-100:])  # Last 100 steps
        
        # Create tabs for different chart views
        tab1, tab2, tab3 = st.tabs(["🎯 Key Metrics", "🔄 Real-time", "📊 Distribution"])
        
        with tab1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_history['step'], y=df_history['comfort'],
                                   name='Comfort', line=dict(color='green')))
            fig.add_trace(go.Scatter(x=df_history['step'], y=df_history['energy']/5,
                                   name='Energy (÷5)', line=dict(color='red')))
            fig.add_trace(go.Scatter(x=df_history['step'], y=df_history['user_satisfaction'],
                                   name='User Satisfaction', line=dict(color='blue')))
            
            fig.add_hline(y=comfort_target, line_dash="dash", line_color="green", 
                         annotation_text="Comfort Target")
            fig.update_layout(title="Key Performance Metrics Over Time", height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Real-time gauge charts
            col1, col2 = st.columns(2)
            
            with col1:
                current_comfort = df_history['comfort'].iloc[-1]
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = current_comfort,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Current Comfort Level"},
                    delta = {'reference': comfort_target},
                    gauge = {
                        'axis': {'range': [None, 1]},
                        'bar': {'color': "darkblue"},
                        'steps': [{'range': [0, 0.5], 'color': "lightgray"},
                                 {'range': [0.5, 0.7], 'color': "yellow"},
                                 {'range': [0.7, 1], 'color': "green"}],
                        'threshold': {'line': {'color': "red", 'width': 4},
                                     'thickness': 0.75, 'value': comfort_target}
                    }
                ))
                fig_gauge.update_layout(height=300)
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col2:
                current_energy = df_history['energy'].iloc[-1]
                fig_gauge2 = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = current_energy,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Current Energy Usage"},
                    delta = {'reference': energy_limit},
                    gauge = {
                        'axis': {'range': [0, 8]},
                        'bar': {'color': "orange"},
                        'steps': [{'range': [0, 2], 'color': "green"},
                                 {'range': [2, 4], 'color': "yellow"},
                                 {'range': [4, 8], 'color': "red"}],
                        'threshold': {'line': {'color': "red", 'width': 4},
                                     'thickness': 0.75, 'value': energy_limit}
                    }
                ))
                fig_gauge2.update_layout(height=300)
                st.plotly_chart(fig_gauge2, use_container_width=True)
        
        with tab3:
            # Action distribution
            action_names = {0: "⏸️ Nothing", 1: "🌀 Fan On", 2: "🌀 Fan Off", 
                          3: "💡 Light Up", 4: "💡 Light Down"}
            df_history['action_name'] = df_history['action'].map(action_names)
            
            fig_pie = px.pie(df_history['action_name'].value_counts().reset_index(), 
                           values='count', names='action_name',
                           title="Action Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)

# Auto-refresh
if monitoring_enabled:
    time.sleep(update_frequency)
    st.rerun()

# Control buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Reset Monitoring"):
        st.session_state.validator = RealTimeValidator()
        st.session_state.step_count = 0
        st.session_state.obs, _ = env.reset()
        st.rerun()

with col2:
    if st.button("💾 Export Data"):
        if len(validator.performance_history) > 0:
            df_export = pd.DataFrame(validator.performance_history)
            csv = df_export.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"ai_performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

with col3:
    if st.button("📊 Generate Report"):
        if len(validator.performance_history) > 0:
            summary = validator.get_performance_summary(len(validator.performance_history))
            st.json(summary)