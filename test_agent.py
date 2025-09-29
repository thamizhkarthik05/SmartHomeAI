import gymnasium as gym
from stable_baselines3 import DQN
from environment import SmartHomeEnv
import time

# --- LOAD THE TRAINED AGENT ---
model_path = "smart_home_ai_brain.zip"
model = DQN.load(model_path)
print("✅ Model loaded successfully!")

# --- CREATE THE ENVIRONMENT ---
# Use the same environment class the model was trained on
env = SmartHomeEnv(data_file="SmartHome_Environment_v1.csv")

# --- TEST THE AGENT ---
obs, info = env.reset()
terminated = False
total_reward = 0

# Action meanings for better readability
action_meanings = {
    0: "Do Nothing",
    1: "Turn Fan ON",
    2: "Turn Fan OFF",
    3: "Increase Light by 20%",
    4: "Decrease Light by 20%"
}

print("\n🤖 --- Testing AI Agent --- 🤖\n")

while not terminated:
    # The model uses its policy to predict the best action
    action, _states = model.predict(obs, deterministic=True)
    
    # The environment executes the action and returns the next state, reward, etc.
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Print the results of the step
    print(f"Step {env.current_step}:")
    print(f"  - Temp: {obs[0]:.1f}°C, Light: {obs[2]:.0f} lux, Comfort: {obs[3]:.2f}")
    print(f"  - AI Action: {int(action)} ({action_meanings.get(int(action), 'Unknown')})")
    print(f"  - Reward for this step: {reward:.2f}")
    print("-" * 20)
    
    total_reward += reward
    
    # Optional: add a small delay to make it easier to read the output
    time.sleep(0.1)

print(f"\n🏁 --- Test Complete --- 🏁")
print(f"Total reward accumulated: {total_reward:.2f}")

env.close()