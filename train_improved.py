import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnNoModelImprovement
from interactive_environment import InteractiveSmartHomeEnv

print("="*70)
print("🏠 SMART HOME AI - IMPROVED TRAINING")
print("="*70)

print("\n✨ Key Improvements:")
print("   ✅ Actions have REAL effects on environment")
print("   ✅ Temperature changes when HVAC is toggled")
print("   ✅ Lighting changes when light actions are taken")
print("   ✅ Comfort updates based on current conditions")
print("   ✅ Better reward function (no action penalty!)")
print("   ✅ Increased exploration (50% of training)")

# Create the interactive environment
print("\n🏗️  Creating interactive environment...")
env = InteractiveSmartHomeEnv()
print("✅ Interactive environment created!")

# Create evaluation environment
eval_env = InteractiveSmartHomeEnv()

# Setup callbacks for better training
stop_callback = StopTrainingOnNoModelImprovement(max_no_improvement_evals=5, min_evals=10, verbose=1)
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path='./logs/',
    log_path='./logs/',
    eval_freq=5000,
    deterministic=True,
    render=False,
    callback_after_eval=stop_callback,
    verbose=1
)

# Create the DQN model with IMPROVED hyperparameters
print("\n🧠 Creating AI model with improved parameters...")
model = DQN(
    policy="MlpPolicy", 
    env=env, 
    verbose=1, 
    learning_rate=0.001,           # Higher learning rate
    buffer_size=50000,             # Larger replay buffer
    learning_starts=1000,          # Start learning earlier
    batch_size=128,                # Larger batches
    gamma=0.99,                    # Standard discount factor
    train_freq=4,                  # Update frequency
    target_update_interval=500,    # More frequent target updates
    exploration_fraction=0.5,      # 🔥 EXPLORE FOR 50% OF TRAINING!
    exploration_initial_eps=1.0,   # Start fully random
    exploration_final_eps=0.1,     # End with 10% randomness
    tensorboard_log="./tensorboard_logs/"
)

print("✅ Model created with better exploration!")
print("\n🎯 Training Configuration:")
print(f"   Learning rate:      0.001")
print(f"   Buffer size:        50,000")
print(f"   Batch size:         128")
print(f"   Total timesteps:    200,000")
print(f"   Exploration:        50% of training 🔥")
print(f"   Final randomness:   10%")

# Train the model
print("\n🚀 Training started... this may take 10-20 minutes!")
print("-"*70)

try:
    model.learn(
        total_timesteps=200000,  # More training!
        callback=eval_callback,
        progress_bar=True
    )
    print("\n✅ Training complete!")
except KeyboardInterrupt:
    print("\n⚠️ Training interrupted by user")

# Save the trained model
model.save("smart_home_ai_brain_v2")
print("💾 Model saved as smart_home_ai_brain_v2.zip")

# Test the model
print("\n" + "="*70)
print("🧪 QUICK TEST")
print("="*70)

from collections import Counter
action_counts = Counter()

obs, _ = env.reset()
for _ in range(100):
    action, _ = model.predict(obs, deterministic=True)
    action_counts[int(action)] += 1
    obs, reward, done, truncated, info = env.step(action)
    if done:
        obs, _ = env.reset()

ACTION_NAMES = {
    0: "Do Nothing",
    1: "HVAC On",
    2: "HVAC Off",
    3: "Light +",
    4: "Light -"
}

print("\nAction Distribution (100 test steps):")
for action_id, count in sorted(action_counts.items()):
    percentage = (count / 100) * 100
    print(f"  {ACTION_NAMES[action_id]:15s}: {count:3d} times ({percentage:5.1f}%)")

print("\n" + "="*70)
print("🎉 TRAINING COMPLETE!")
print("="*70)
print("\n🚀 Next steps:")
print("   1. Test improved model: python test_improved_model.py")
print("   2. Run dashboard with new model")
print("="*70)
