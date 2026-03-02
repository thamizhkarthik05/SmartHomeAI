"""
Analyze DQN Model Behavior and Action Distribution
This script will help diagnose why the model only chooses "Do Nothing"
"""

import numpy as np
from stable_baselines3 import DQN
from environment import SmartHomeEnv
import pandas as pd
from collections import Counter

print("="*70)
print("🔍 DQN MODEL BEHAVIOR ANALYSIS")
print("="*70)

# Load the trained model
print("\n📥 Loading model...")
try:
    model = DQN.load("smart_home_ai_brain")
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit(1)

# Create environment
print("\n🏠 Creating environment...")
env = SmartHomeEnv(data_file="SmartHome_Realistic_Dataset.csv")
print(f"✅ Dataset loaded: {len(env.df):,} samples")

# Action names
ACTION_NAMES = {
    0: "Do Nothing",
    1: "Turn Fan On",
    2: "Turn Fan Off",
    3: "Increase Light",
    4: "Decrease Light"
}

print("\n" + "="*70)
print("📊 TESTING MODEL BEHAVIOR")
print("="*70)

# Test the model for multiple episodes
num_test_steps = 500
action_counts = Counter()
action_rewards = {i: [] for i in range(5)}
state_samples = []

obs, _ = env.reset()

print("\n🎯 Running 500 test steps...\n")

for step in range(num_test_steps):
    # Get action from model
    action, _ = model.predict(obs, deterministic=True)
    action = int(action)
    
    # Take step
    next_obs, reward, done, truncated, info = env.step(action)
    
    # Track statistics
    action_counts[action] += 1
    action_rewards[action].append(reward)
    
    # Save some sample states and actions
    if step < 20 or (step % 50 == 0):
        state_samples.append({
            'step': step,
            'temp': obs[0],
            'perceived_temp': obs[1],
            'light': obs[2],
            'comfort': obs[3],
            'fan_state': obs[4],
            'light_percent': obs[5],
            'energy': obs[6],
            'action': ACTION_NAMES[action],
            'reward': reward
        })
    
    if done:
        obs, _ = env.reset()
    else:
        obs = next_obs

# Print results
print("="*70)
print("📈 ACTION DISTRIBUTION")
print("="*70)

total_actions = sum(action_counts.values())
for action_id in range(5):
    count = action_counts[action_id]
    percentage = (count / total_actions) * 100
    avg_reward = np.mean(action_rewards[action_id]) if action_rewards[action_id] else 0
    print(f"\n{ACTION_NAMES[action_id]:20s}: {count:4d} times ({percentage:5.1f}%)")
    print(f"{'':20s}  Avg Reward: {avg_reward:+.3f}")

print("\n" + "="*70)
print("🎬 SAMPLE DECISIONS (First 20 steps)")
print("="*70)

for sample in state_samples[:20]:
    print(f"\nStep {sample['step']:3d}:")
    print(f"  Temp: {sample['temp']:.1f}°C, Comfort: {sample['comfort']:.3f}, Fan: {'ON' if sample['fan_state'] else 'OFF'}")
    print(f"  Light: {sample['light']:.0f} lux ({sample['light_percent']:.0f}%), Energy: {sample['energy']:.1f} kW")
    print(f"  → Action: {sample['action']} | Reward: {sample['reward']:+.2f}")

print("\n" + "="*70)
print("🔬 REWARD FUNCTION ANALYSIS")
print("="*70)

# Analyze the reward structure
print("\nReward Formula in environment.py:")
print("  reward = comfort_score * 10")
print("         - energy_consumed * 2")
print("         - user_override * 20")
print("         - action_penalty * 0.5 (if action != 0)")

# Calculate average rewards for each component
comfort_values = []
energy_values = []
override_values = []

obs, _ = env.reset()
for _ in range(100):
    row = env.df.iloc[env.current_step]
    comfort_values.append(row["comfort_score"] * 10)
    energy_values.append(row["energy_consumed_kw"] * 2)
    override_values.append(row["user_override_event"] * 20)
    env.step(0)

print(f"\nAverage Comfort Reward:   +{np.mean(comfort_values):.2f}")
print(f"Average Energy Penalty:   -{np.mean(energy_values):.2f}")
print(f"Average Override Penalty: -{np.mean(override_values):.2f}")
print(f"Action Penalty (if taken): -0.50")

print("\n" + "="*70)
print("💡 DIAGNOSIS")
print("="*70)

if action_counts[0] > total_actions * 0.8:
    print("\n⚠️  MODEL IS STUCK IN 'DO NOTHING' MODE!")
    print("\n🔍 Possible Reasons:")
    print("\n1. ❌ REWARD FUNCTION ISSUE:")
    print("   - Action penalty (-0.5) discourages any action")
    print("   - The model learned that doing nothing avoids the penalty")
    print("   - Energy penalty might be too high relative to comfort reward")
    
    print("\n2. ❌ TRAINING ISSUE:")
    print("   - Model didn't explore enough actions during training")
    print("   - May need more training timesteps")
    print("   - Exploration parameters might be too conservative")
    
    print("\n3. ❌ DATASET ISSUE:")
    print("   - Fan is ALWAYS ON in dataset (fan_state = on)")
    print("   - Light and energy values don't change with actions")
    print("   - Model doesn't see cause-and-effect of its actions")
    
    print("\n" + "="*70)
    print("✅ RECOMMENDED FIXES")
    print("="*70)
    
    print("\n1. FIX ENVIRONMENT.PY - Make actions have real effects:")
    print("   - Change temperature when fan is toggled")
    print("   - Change light levels when light actions are taken")
    print("   - Update comfort and energy based on these changes")
    
    print("\n2. IMPROVE REWARD FUNCTION:")
    print("   - Reduce or remove action penalty")
    print("   - Add positive rewards for good actions")
    print("   - Reward achieving target temperature/lighting")
    
    print("\n3. RETRAIN WITH BETTER EXPLORATION:")
    print("   - Increase exploration_fraction to 0.5")
    print("   - Increase total_timesteps to 200,000")
    print("   - Use more diverse initial conditions")

else:
    print("\n✅ Model shows diverse action distribution")
    print("   Training appears successful")

print("\n" + "="*70)
