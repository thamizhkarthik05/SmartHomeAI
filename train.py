import gymnasium as gym
from stable_baselines3 import DQN
from environment import SmartHomeEnv

# Create the environment
env = SmartHomeEnv(data_file="SmartHome_Environment_v1.csv")

# Create the DQN model
model = DQN(
    policy="MlpPolicy", 
    env=env, 
    verbose=1, 
    learning_rate=0.001,
    buffer_size=5000,
    learning_starts=1000,
    batch_size=32,
    gamma=0.99,
    train_freq=4,
    target_update_interval=1000
)

# Train the model
print("🚀 Training started... this may take a while!")
model.learn(total_timesteps=50000)

# Save the trained model (AI's brain)
model.save("smart_home_ai_brain")
print("✅ Training complete! Model saved as smart_home_ai_brain.zip")
