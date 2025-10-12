import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import EvalCallback, StopTrainingOnNoModelImprovement
from environment import SmartHomeEnv

print("="*60)
print("🏠 SMART HOME AI TRAINING")
print("="*60)

# Create the environment with NEW realistic dataset
print("\n📊 Loading dataset...")
env = SmartHomeEnv(data_file="SmartHome_Realistic_Dataset.csv")
print(f"✅ Dataset loaded: {len(env.df):,} samples")

# Create evaluation environment
eval_env = SmartHomeEnv(data_file="SmartHome_Realistic_Dataset.csv")

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

# Create the DQN model with optimized hyperparameters
print("\n🧠 Creating AI model...")
model = DQN(
    policy="MlpPolicy", 
    env=env, 
    verbose=1, 
    learning_rate=0.0005,      # Slightly lower for stability
    buffer_size=20000,         # Larger buffer for more diverse experiences
    learning_starts=2000,      # Start learning after collecting good experiences
    batch_size=64,             # Larger batches for better learning
    gamma=0.99,                # Standard discount factor
    train_freq=4,              # Update frequency
    target_update_interval=1000,
    exploration_fraction=0.3,  # Explore for 30% of training
    exploration_initial_eps=1.0,
    exploration_final_eps=0.05,
    tensorboard_log="./tensorboard_logs/"
)

print("✅ Model created")
print("\n🎯 Training Configuration:")
print(f"   Learning rate: 0.0005")
print(f"   Buffer size: 20,000")
print(f"   Batch size: 64")
print(f"   Total timesteps: 100,000")
print(f"   Exploration: 30% of training")

# Train the model
print("\n🚀 Training started... this may take 5-15 minutes!")
print("-"*60)

try:
    model.learn(
        total_timesteps=100000,  # More training for better learning
        callback=eval_callback,
        progress_bar=True
    )
    print("\n✅ Training complete!")
except KeyboardInterrupt:
    print("\n⚠️ Training interrupted by user")

# Save the trained model (AI's brain)
model.save("smart_home_ai_brain")
print("💾 Model saved as smart_home_ai_brain.zip")

print("\n"+"="*60)
print("🎉 TRAINING COMPLETE!")
print("="*60)
print("\n🚀 Next steps:")
print("   1. Test the model: python test_agent.py")
print("   2. Validate performance: python ai_validator.py")
print("   3. Run dashboard: streamlit run enhanced_dashboard.py")
print("="*60)
