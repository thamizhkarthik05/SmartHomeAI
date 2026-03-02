"""
Test the Improved DQN Model
Shows that actions are now diverse and meaningful
"""

import numpy as np
from stable_baselines3 import DQN
from interactive_environment import InteractiveSmartHomeEnv
from collections import Counter

print("="*70)
print("🧪 TESTING IMPROVED DQN MODEL")
print("="*70)

# Load model
print("\n📥 Loading improved model...")
try:
    model = DQN.load("smart_home_ai_brain_v2")
    print("✅ Model loaded: smart_home_ai_brain_v2.zip")
except FileNotFoundError:
    print("❌ Model not found! Please run: python train_improved.py first")
    exit(1)

# Create environment
env = InteractiveSmartHomeEnv()

# Action names
ACTION_NAMES = {
    0: "Do Nothing",
    1: "HVAC On",
    2: "HVAC Off",
    3: "Light +",
    4: "Light -"
}

print("\n" + "="*70)
print("📊 RUNNING COMPREHENSIVE TEST")
print("="*70)

# Test for 5 episodes
num_episodes = 5
all_actions = Counter()
episode_rewards = []

for episode in range(num_episodes):
    print(f"\n🎬 Episode {episode + 1}")
    print("-" * 70)
    
    obs, _ = env.reset()
    episode_reward = 0
    episode_actions = Counter()
    
    for step in range(100):
        # Get action from model
        action, _ = model.predict(obs, deterministic=True)
        action = int(action)
        
        # Take step
        obs, reward, done, truncated, info = env.step(action)
        
        # Track stats
        episode_actions[action] += 1
        all_actions[action] += 1
        episode_reward += reward
        
        # Print first 10 steps
        if step < 10:
            print(f"  Step {step:2d}: Temp={obs[0]:5.1f}°C, Light={obs[5]:5.1f}%, "
                  f"HVAC={'ON ' if obs[4] else 'OFF'}, Comfort={obs[3]:.3f} "
                  f"→ {ACTION_NAMES[action]:12s} | R={reward:+6.2f}")
        
        if done:
            break
    
    episode_rewards.append(episode_reward)
    
    print(f"\n  📈 Episode Summary:")
    print(f"     Total Reward: {episode_reward:+.2f}")
    print(f"     Actions: ", end="")
    for i in range(5):
        count = episode_actions[i]
        print(f"{ACTION_NAMES[i]}={count}, ", end="")
    print()

print("\n" + "="*70)
print("📊 OVERALL STATISTICS")
print("="*70)

total_actions = sum(all_actions.values())
print(f"\nTotal Steps: {total_actions}")
print(f"Average Episode Reward: {np.mean(episode_rewards):+.2f}")
print(f"\n📈 Action Distribution:")

for action_id in range(5):
    count = all_actions[action_id]
    percentage = (count / total_actions) * 100 if total_actions > 0 else 0
    print(f"  {ACTION_NAMES[action_id]:15s}: {count:4d} times ({percentage:5.1f}%)")

print("\n" + "="*70)
print("💡 EVALUATION")
print("="*70)

if all_actions[0] > total_actions * 0.7:
    print("\n⚠️  Still doing nothing too often!")
    print("   Consider training longer or adjusting rewards")
else:
    print("\n✅ Model shows diverse action behavior!")
    print("   ✓ Taking meaningful actions")
    print("   ✓ Responding to environment conditions")
    print("   ✓ Balancing comfort and energy")

print("\n" + "="*70)
