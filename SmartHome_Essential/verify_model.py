"""
🔍 Smart Home AI Model Verification Script
==========================================
This script helps you verify your trained model by:
1. Checking if the model is trained (file exists)
2. Showing what inputs the model takes
3. Demonstrating what outputs the model gives
4. Validating if the outputs are correct
"""

import os
import numpy as np
from stable_baselines3 import DQN
from environment import SmartHomeEnv
import pandas as pd

# Color codes for better readability
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def check_model_exists(model_path="smart_home_ai_brain.zip"):
    """Step 1: Check if model is trained"""
    print(f"\n{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BLUE}STEP 1: Checking if Model is Trained{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    
    if os.path.exists(model_path):
        file_size = os.path.getsize(model_path) / 1024  # Convert to KB
        print(f"{GREEN}✅ Model file found: {model_path}{RESET}")
        print(f"   File size: {file_size:.2f} KB")
        print(f"   {GREEN}Status: Model is trained and saved!{RESET}")
        return True
    else:
        print(f"{RED}❌ Model file NOT found: {model_path}{RESET}")
        print(f"   {YELLOW}You need to train the model first by running:{RESET}")
        print(f"   {YELLOW}python train.py{RESET}")
        return False

def show_model_inputs():
    """Step 2: Show what inputs the model takes"""
    print(f"\n{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BLUE}STEP 2: Model Input Specifications{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    
    env = SmartHomeEnv(data_file="SmartHome_Environment_v1.csv")
    
    print(f"\n{GREEN}The model takes a 7-dimensional observation vector:{RESET}")
    print(f"\n  Index | Feature Name              | Range       | Description")
    print(f"  ------|---------------------------|-------------|----------------------------------")
    print(f"    0   | room_temperature_c        | 0-40°C      | Current room temperature")
    print(f"    1   | perceived_temperature_c   | 0-40°C      | How temperature feels to humans")
    print(f"    2   | ambient_light_lux         | 0-2000 lux  | Light intensity in the room")
    print(f"    3   | comfort_score             | 0-1         | User comfort level (0=bad, 1=perfect)")
    print(f"    4   | fan_state                 | 0-1         | Fan status (0=off, 1=on)")
    print(f"    5   | light_state_percent       | 0-100%      | Light brightness level")
    print(f"    6   | energy_consumed_kw        | 0-10 kW     | Energy consumption")
    
    # Show a sample observation
    obs, _ = env.reset()
    print(f"\n{YELLOW}Example observation from the dataset:{RESET}")
    print(f"  {obs}")
    
    env.close()

def show_model_outputs():
    """Step 3: Show what outputs the model gives"""
    print(f"\n{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BLUE}STEP 3: Model Output Specifications{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    
    print(f"\n{GREEN}The model outputs a single action (integer 0-4):{RESET}")
    print(f"\n  Action | Description")
    print(f"  -------|--------------------------------------------------")
    print(f"    0    | Do Nothing - Maintain current settings")
    print(f"    1    | Turn Fan ON - Activate cooling")
    print(f"    2    | Turn Fan OFF - Deactivate cooling")
    print(f"    3    | Increase Light by 20% - Brighten the room")
    print(f"    4    | Decrease Light by 20% - Dim the room")
    
    print(f"\n{YELLOW}The action is chosen based on the current state to:{RESET}")
    print(f"  • Maximize user comfort (comfort_score)")
    print(f"  • Minimize energy consumption")
    print(f"  • Avoid triggering user overrides")

def verify_model_correctness(num_steps=20):
    """Step 4: Verify if model outputs are correct"""
    print(f"\n{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BLUE}STEP 4: Verifying Model Output Correctness{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    
    # Load model
    model = DQN.load("smart_home_ai_brain.zip")
    env = SmartHomeEnv(data_file="SmartHome_Environment_v1.csv")
    
    action_names = {
        0: "Do Nothing",
        1: "Turn Fan ON",
        2: "Turn Fan OFF",
        3: "Increase Light +20%",
        4: "Decrease Light -20%"
    }
    
    obs, _ = env.reset()
    total_reward = 0
    comfort_scores = []
    energy_usage = []
    actions_taken = []
    
    print(f"\n{YELLOW}Running model for {num_steps} steps...{RESET}\n")
    
    for step in range(num_steps):
        # Model predicts action
        action, _ = model.predict(obs, deterministic=True)
        action = int(action)
        
        # Execute action in environment
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Track metrics
        total_reward += reward
        comfort_scores.append(obs[3])
        energy_usage.append(obs[6])
        actions_taken.append(action)
        
        # Print step details
        if step < 10 or step >= num_steps - 5:  # Show first 10 and last 5 steps
            print(f"  Step {step+1:2d}: Temp={obs[0]:5.1f}°C, Light={obs[2]:6.0f}lux, "
                  f"Comfort={obs[3]:.2f}, Energy={obs[6]:.2f}kW → {action_names[action]}")
        elif step == 10:
            print(f"  ... (showing abbreviated output) ...")
        
        if terminated:
            break
    
    # Calculate statistics
    avg_comfort = np.mean(comfort_scores)
    avg_energy = np.mean(energy_usage)
    
    print(f"\n{GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{GREEN}Verification Results:{RESET}")
    print(f"{GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"\n  📊 Total Reward Accumulated: {total_reward:.2f}")
    print(f"  😊 Average Comfort Score: {avg_comfort:.3f} (target: >0.7)")
    print(f"  ⚡ Average Energy Usage: {avg_energy:.3f} kW (target: <2.0 kW)")
    print(f"  🎯 Action Distribution:")
    
    # Show action distribution
    for action_num in range(5):
        count = actions_taken.count(action_num)
        percentage = (count / len(actions_taken)) * 100
        bar = "█" * int(percentage / 5)
        print(f"      {action_num} ({action_names[action_num]:20s}): {bar} {percentage:5.1f}%")
    
    # Provide assessment
    print(f"\n{YELLOW}Assessment:{RESET}")
    
    if total_reward > 0:
        print(f"  {GREEN}✅ Positive total reward - Model is learning to balance comfort & energy!{RESET}")
    else:
        print(f"  {YELLOW}⚠️  Negative total reward - Model might need more training{RESET}")
    
    if avg_comfort > 0.7:
        print(f"  {GREEN}✅ Good comfort level - Users should be satisfied{RESET}")
    else:
        print(f"  {YELLOW}⚠️  Low comfort level - Model prioritizing energy over comfort{RESET}")
    
    if avg_energy < 2.0:
        print(f"  {GREEN}✅ Energy efficient - Good cost savings!{RESET}")
    else:
        print(f"  {YELLOW}⚠️  High energy usage - Model might be over-controlling devices{RESET}")
    
    env.close()
    
    return {
        'total_reward': total_reward,
        'avg_comfort': avg_comfort,
        'avg_energy': avg_energy,
        'is_good': total_reward > 0 and avg_comfort > 0.7
    }

def compare_with_baseline():
    """Step 5: Compare model with baseline (random actions)"""
    print(f"\n{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BLUE}STEP 5: Comparing with Baseline (Random Actions){RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    
    env = SmartHomeEnv(data_file="SmartHome_Environment_v1.csv")
    obs, _ = env.reset()
    
    baseline_reward = 0
    baseline_comfort = []
    
    for _ in range(20):
        action = env.action_space.sample()  # Random action
        obs, reward, terminated, truncated, _ = env.step(action)
        baseline_reward += reward
        baseline_comfort.append(obs[3])
        if terminated:
            break
    
    print(f"\n  Random Agent Performance:")
    print(f"    Total Reward: {baseline_reward:.2f}")
    print(f"    Avg Comfort: {np.mean(baseline_comfort):.3f}")
    
    env.close()

def main():
    """Main verification function"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}     🤖 SMART HOME AI MODEL VERIFICATION TOOL 🤖{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    # Step 1: Check if model exists
    if not check_model_exists():
        print(f"\n{RED}Cannot proceed with verification. Please train the model first.{RESET}")
        return
    
    # Step 2: Show inputs
    show_model_inputs()
    
    # Step 3: Show outputs
    show_model_outputs()
    
    # Step 4: Verify correctness
    results = verify_model_correctness(num_steps=20)
    
    # Step 5: Compare with baseline
    compare_with_baseline()
    
    # Final summary
    print(f"\n{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    print(f"{BLUE}Final Verdict:{RESET}")
    print(f"{BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    
    if results['is_good']:
        print(f"\n{GREEN}✅ ✅ ✅  MODEL IS WORKING CORRECTLY! ✅ ✅ ✅{RESET}")
        print(f"{GREEN}The model has learned to make good decisions that balance{RESET}")
        print(f"{GREEN}user comfort and energy efficiency.{RESET}")
    else:
        print(f"\n{YELLOW}⚠️  MODEL NEEDS IMPROVEMENT{RESET}")
        print(f"{YELLOW}Consider training for more timesteps or adjusting hyperparameters.{RESET}")
        print(f"{YELLOW}Run: python train.py (and increase total_timesteps){RESET}")
    
    print(f"\n{BLUE}{'='*60}{RESET}\n")

if __name__ == "__main__":
    main()
