# 🔍 Smart Home AI Model Verification Guide

## Overview

This guide explains how to verify your trained Smart Home AI model, understand its inputs/outputs, and validate that it's working correctly.

---

## Quick Start

### 1. Check if Model is Trained

```bash
# Check if the model file exists
ls -l smart_home_ai_brain.zip
```

If the file doesn't exist, train it first:
```bash
python train.py
```

### 2. Run Verification Script

```bash
python verify_model.py
```

This comprehensive script will:
- ✅ Check if your model is trained
- 📊 Show what inputs the model takes
- 🎯 Demonstrate what outputs it produces
- 🔬 Verify if the outputs are correct
- 📈 Compare with baseline performance

---

## Understanding Your Model

### Model Architecture

- **Type**: Deep Q-Network (DQN)
- **Framework**: Stable Baselines3
- **Policy**: MLP (Multi-Layer Perceptron)
- **Input Dimension**: 7 features
- **Output Dimension**: 5 discrete actions

### Training Configuration

From `train.py`:
```python
model = DQN(
    policy="MlpPolicy", 
    env=env, 
    learning_rate=0.001,
    buffer_size=5000,
    learning_starts=1000,
    batch_size=32,
    gamma=0.99,
    train_freq=4,
    target_update_interval=1000
)
model.learn(total_timesteps=50000)
```

---

## Model Inputs (State Space)

The model receives a 7-dimensional observation vector representing the current state:

| Index | Feature Name              | Range      | Description                              |
|-------|---------------------------|------------|------------------------------------------|
| 0     | `room_temperature_c`      | 0-40°C     | Current room temperature                 |
| 1     | `perceived_temperature_c` | 0-40°C     | How temperature feels to humans          |
| 2     | `ambient_light_lux`       | 0-2000 lux | Light intensity in the room              |
| 3     | `comfort_score`           | 0-1        | User comfort level (0=bad, 1=perfect)    |
| 4     | `fan_state`               | 0-1        | Fan status (0=off, 1=on)                 |
| 5     | `light_state_percent`     | 0-100      | Light brightness level                   |
| 6     | `energy_consumed_kw`      | 0-10 kW    | Energy consumption                       |

### Example Input
```python
obs = [25.3, 26.1, 450.0, 0.85, 0.0, 60.0, 1.2]
# Temperature: 25.3°C, Light: 450 lux, Comfort: 0.85, etc.
```

---

## Model Outputs (Action Space)

The model outputs a single integer (0-4) representing the action to take:

| Action | Description                | When Used                                    |
|--------|----------------------------|----------------------------------------------|
| 0      | Do Nothing                 | Current conditions are optimal               |
| 1      | Turn Fan ON                | Room is too hot                              |
| 2      | Turn Fan OFF               | Room is cool enough, save energy             |
| 3      | Increase Light by 20%      | Room is too dark for comfort                 |
| 4      | Decrease Light by 20%      | Room is too bright or saving energy          |

### Example Usage
```python
from stable_baselines3 import DQN

# Load trained model
model = DQN.load("smart_home_ai_brain.zip")

# Given a state observation
obs = [27.5, 28.2, 300.0, 0.65, 0, 40.0, 0.8]

# Model predicts the best action
action, _ = model.predict(obs, deterministic=True)
print(f"Action: {action}")  # e.g., outputs 1 (Turn Fan ON)
```

---

## How to Verify Model Output is Correct

### Method 1: Run the Verification Script

```bash
python verify_model.py
```

This will automatically:
1. Check model existence
2. Display input/output specifications
3. Run the model for 20 steps
4. Calculate performance metrics
5. Compare with random baseline

**Expected Output:**
```
✅ Positive total reward - Model is learning!
✅ Good comfort level - Users should be satisfied
✅ Energy efficient - Good cost savings!
```

### Method 2: Run the Test Agent

```bash
python test_agent.py
```

This runs the model through the entire dataset and shows:
- Step-by-step decisions
- Temperature, light, and comfort at each step
- Actions taken by the AI
- Total reward accumulated

### Method 3: Manual Verification

Create a simple test script:

```python
from stable_baselines3 import DQN
from environment import SmartHomeEnv

# Load model and environment
model = DQN.load("smart_home_ai_brain.zip")
env = SmartHomeEnv(data_file="SmartHome_Environment_v1.csv")

# Reset environment
obs, _ = env.reset()

# Test for a few steps
for step in range(10):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _, _ = env.step(action)
    
    print(f"Step {step+1}:")
    print(f"  Temperature: {obs[0]:.1f}°C")
    print(f"  Comfort: {obs[3]:.2f}")
    print(f"  Action: {action}")
    print(f"  Reward: {reward:.2f}")
    print()
    
    if done:
        break

env.close()
```

---

## Performance Metrics

### Key Indicators of Correct Model Behavior

1. **Total Reward** (Higher is Better)
   - Positive values indicate good learning
   - Target: > 0
   - Interpretation: Model is successfully balancing comfort and energy

2. **Average Comfort Score** (Higher is Better)
   - Range: 0-1
   - Target: > 0.7
   - Interpretation: Users are satisfied with the environment

3. **Average Energy Consumption** (Lower is Better)
   - Range: 0-10 kW
   - Target: < 2.0 kW
   - Interpretation: Model is energy efficient

4. **Action Distribution**
   - Should show variety (not just one action)
   - "Do Nothing" should be most common (optimal state)
   - Fan/Light controls used when needed

### Expected Behavior Patterns

✅ **Good Model:**
- Turns fan ON when temperature > 26°C
- Turns fan OFF when temperature < 24°C
- Adjusts lights based on ambient light levels
- Maintains high comfort scores (>0.7)
- Minimizes unnecessary actions

❌ **Poor Model (Needs More Training):**
- Random or erratic actions
- Low comfort scores (<0.5)
- High energy consumption (>3 kW)
- Negative total rewards
- Always chooses the same action

---

## Troubleshooting

### Issue: Model File Not Found

**Problem:** `smart_home_ai_brain.zip` doesn't exist

**Solution:**
```bash
python train.py
```
Wait for training to complete (~5-10 minutes)

### Issue: Low Performance Metrics

**Problem:** Model has negative rewards or low comfort

**Solutions:**
1. **Train Longer:**
   ```python
   # In train.py, increase total_timesteps
   model.learn(total_timesteps=100000)  # Instead of 50000
   ```

2. **Adjust Hyperparameters:**
   ```python
   model = DQN(
       learning_rate=0.0005,  # Try different values
       gamma=0.95,            # Adjust discount factor
       buffer_size=10000      # Increase replay buffer
   )
   ```

3. **Check Data Quality:**
   ```bash
   python explore_data.py
   ```
   Ensure dataset has good quality data

### Issue: Model Makes Strange Decisions

**Problem:** Model behavior doesn't make sense

**Diagnostic Steps:**
1. Check reward function in `environment.py`:
   ```python
   # Ensure rewards align with goals
   reward += row["comfort_score"] * 10      # Encourage comfort
   reward -= row["energy_consumed_kw"] * 2   # Penalize energy
   ```

2. Verify action space is correct
3. Check if observations are normalized properly

---

## Advanced Verification

### Visualize Model Decisions

```python
import matplotlib.pyplot as plt

# Track decisions over time
temperatures = []
actions = []
comforts = []

for step in range(100):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _, _ = env.step(action)
    
    temperatures.append(obs[0])
    actions.append(action)
    comforts.append(obs[3])
    
    if done:
        break

# Plot results
plt.figure(figsize=(12, 4))

plt.subplot(131)
plt.plot(temperatures)
plt.title('Temperature Over Time')
plt.ylabel('°C')

plt.subplot(132)
plt.plot(actions)
plt.title('Actions Taken')
plt.ylabel('Action ID')

plt.subplot(133)
plt.plot(comforts)
plt.title('Comfort Score')
plt.ylabel('Score')

plt.tight_layout()
plt.show()
```

### Test Edge Cases

```python
# Test extreme temperature
obs_hot = [35.0, 36.0, 500, 0.3, 0, 60, 2.0]
action, _ = model.predict(obs_hot)
print(f"When very hot: Action {action}")  # Should turn fan ON

# Test extreme cold
obs_cold = [18.0, 17.0, 500, 0.4, 1, 60, 2.5]
action, _ = model.predict(obs_cold)
print(f"When very cold: Action {action}")  # Should turn fan OFF

# Test low light
obs_dark = [24.0, 24.5, 50, 0.6, 0, 20, 0.8]
action, _ = model.predict(obs_dark)
print(f"When dark: Action {action}")  # Should increase light
```

---

## Summary Checklist

Use this checklist to verify your model:

- [ ] Model file exists (`smart_home_ai_brain.zip`)
- [ ] Model loads without errors
- [ ] Model accepts 7-dimensional input
- [ ] Model outputs integers 0-4
- [ ] Total reward is positive
- [ ] Average comfort score > 0.7
- [ ] Average energy usage < 2.0 kW
- [ ] Actions make logical sense (fan ON when hot, etc.)
- [ ] Model performs better than random baseline
- [ ] No errors during testing

---

## Next Steps

Once your model is verified:

1. **Deploy to Dashboard:**
   ```bash
   python dashboard.py
   ```

2. **Test with IoT Devices:**
   ```bash
   python iot_device_simulator.py
   ```

3. **Monitor Performance:**
   ```bash
   python performance_monitor.py
   ```

4. **Run A/B Testing:**
   ```bash
   python ab_testing.py
   ```

---

## Need Help?

If verification fails or you need assistance:

1. Check the reward function in `environment.py`
2. Review training logs for errors
3. Ensure dataset quality is good
4. Try training with different hyperparameters
5. Compare with baseline (random agent)

Remember: A good model should make intuitive decisions that balance user comfort with energy efficiency!
