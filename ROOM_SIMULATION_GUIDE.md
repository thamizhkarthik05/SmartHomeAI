# 🏠 Smart Home Room Simulator Guide

## Overview

The Room Simulator provides a **visual, interactive way** to see your AI model in action! Watch as your AI controls a virtual room with lights and fans, making decisions in real-time to balance comfort and energy efficiency.

---

## Features

### 🎮 Interactive Visual Simulation
- **Real room visualization** with animated fans and lights
- **Temperature thermometer** that changes color based on heat
- **Person icon** showing comfort level with emoji feedback
- **Live graphs** tracking temperature and comfort over time

### 🤖 AI Model Integration
- Watch your trained model make decisions in real-time
- See the reasoning behind each action
- Track rewards and performance metrics
- Compare AI decisions vs manual control

### 🎯 Two Control Modes
1. **AUTO MODE**: AI controls the room automatically
2. **MANUAL MODE**: You control the room with keyboard

---

## Installation

### 1. Install Pygame (if not already installed)

```bash
pip install pygame
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

### 2. Ensure Model is Trained

The simulator needs a trained model:

```bash
python train.py
```

This creates `smart_home_ai_brain.zip`

---

## Running the Simulator

### Basic Usage

```bash
python room_simulator.py
```

A window will open showing:
- **Left side**: Visual room with fan, lights, thermometer, person
- **Right side**: Status panel with metrics and AI decisions
- **Bottom**: Control graphs showing history

---

## Controls

### Keyboard Controls

| Key | Action |
|-----|--------|
| **SPACE** | Pause/Resume simulation |
| **M** | Toggle between AUTO and MANUAL mode |
| **R** | Reset simulation |
| **Q** | Quit simulator |

### Manual Mode Controls (when AUTO is OFF)

| Key | Action |
|-----|--------|
| **0** | Do Nothing |
| **1** | Turn Fan ON |
| **2** | Turn Fan OFF |
| **3** | Increase Light brightness by 20% |
| **4** | Decrease Light brightness by 20% |

---

## Understanding the Display

### Room Visualization (Left Panel)

#### 🌡️ Temperature Indicator (Thermometer)
- **Blue**: Cold (< 20°C)
- **Light Blue**: Cool (20-23°C)
- **Green**: Comfortable (23-26°C)
- **Orange**: Warm (26-29°C)
- **Red**: Hot (> 29°C)

The room background color also changes to reflect temperature!

#### 💡 Ceiling Light
- **Brightness**: Shows current light level
- **Glow effect**: Increases with brightness
- **Yellow bulb**: Active (>50% brightness)
- **Gray bulb**: Dim (<50% brightness)

#### 🌀 Ceiling Fan
- **Spinning blades**: Fan is ON and cooling
- **Static blades**: Fan is OFF
- Animation speed shows fan activity

#### 👤 Person Icon
- **Color coding**:
  - 🟢 Green: Comfortable (comfort > 0.7)
  - 🟠 Orange: Moderate (comfort 0.5-0.7)
  - 🔴 Red: Uncomfortable (comfort < 0.5)
- **Emoji face**: Shows comfort level
  - 😊 Happy (comfortable)
  - 😐 Neutral (okay)
  - 😟 Unhappy (uncomfortable)

### Status Panel (Right Side)

#### Metrics Display

**🌡️ Temperature**: Current room temperature in Celsius

**💡 Light**: Ambient light level (lux) and brightness percentage

**😊 Comfort Score**: 
- Visual bar showing comfort level (0-1)
- Green bar: Good comfort (>0.7)
- Orange bar: Moderate comfort (0.5-0.7)
- Red bar: Poor comfort (<0.5)

**⚡ Energy**: Current energy consumption in kilowatts

**Fan Status**: 
- 🟢 ON 🌀 (actively cooling)
- 🔴 OFF (not running)

#### AI Decision Section

**🤖 AI Decision Panel**:
- **Action**: What the AI just decided to do
- **Reward**: Points earned for this action
- **Total Reward**: Cumulative score
- **Step**: Current timestep in simulation

### History Graphs (Bottom)

- **Red line**: Temperature over time
- **Green line**: Comfort level over time
- Shows last 50 timesteps
- Updates in real-time as simulation progresses

---

## How the AI Works

### What the AI Observes
The AI sees 7 features:
1. Room temperature
2. Perceived temperature (how it feels)
3. Ambient light level
4. Current comfort score
5. Fan state (on/off)
6. Light brightness level
7. Energy consumption

### What the AI Decides
Based on observations, the AI chooses one of 5 actions:
- **Do Nothing**: Maintain current settings
- **Turn Fan ON**: Cool the room
- **Turn Fan OFF**: Save energy
- **Increase Light**: Brighten the room
- **Decrease Light**: Dim or save energy

### AI Goals
The AI tries to:
- ✅ **Maximize comfort**: Keep temperature and lighting optimal
- ✅ **Minimize energy**: Use fans and lights efficiently
- ✅ **Avoid waste**: Don't make unnecessary changes

---

## Usage Scenarios

### Scenario 1: Watch AI in Action (AUTO MODE)

1. Start the simulator:
   ```bash
   python room_simulator.py
   ```

2. Let it run in AUTO MODE (default)

3. Observe:
   - How AI responds to temperature changes
   - When it turns fan on/off
   - How it adjusts lighting
   - Comfort level trends
   - Total reward accumulation

4. Press **SPACE** to pause and examine state

### Scenario 2: Compare with Manual Control

1. Press **M** to switch to MANUAL MODE

2. Try controlling the room yourself:
   - Press **1** when it's hot (turn fan on)
   - Press **2** when it's cool (turn fan off)
   - Press **3** when it's dark (increase light)
   - Press **4** when it's bright (decrease light)

3. Watch your reward scores vs AI's scores

4. Press **M** to switch back to AUTO and compare

### Scenario 3: Test Edge Cases

1. Let simulation run until extreme conditions:
   - Very hot room (>30°C)
   - Very cold room (<18°C)
   - Very dark (<100 lux)
   - Very bright (>1000 lux)

2. Observe how AI handles extremes

3. Press **R** to reset and try again

### Scenario 4: Performance Analysis

1. Run for 100+ steps in AUTO MODE

2. Monitor the graphs:
   - Is temperature stabilizing?
   - Is comfort improving over time?
   - Is energy usage reasonable?

3. Check total reward at bottom of status panel
   - Positive = Good performance
   - Negative = Model needs more training

---

## Interpreting Results

### Good AI Performance

✅ **Comfort stays high** (>0.7, green bar)
- Person icon is green 😊
- Minimal complaints

✅ **Temperature in optimal range** (22-25°C)
- Room color is green/light blue
- Thermometer in middle range

✅ **Energy usage is reasonable** (<2.0 kW)
- Fan runs only when needed
- Lights adjust appropriately

✅ **Total reward is positive and growing**
- AI is learning effective strategies
- Good balance of comfort vs energy

### Poor AI Performance (Needs More Training)

❌ **Comfort is low** (<0.5, red bar)
- Person icon is red 😟
- Room conditions uncomfortable

❌ **Temperature extremes** (<20°C or >28°C)
- Room color is blue or red
- AI not responding to temperature

❌ **High energy waste** (>3.0 kW)
- Fan always on
- Lights at max unnecessarily

❌ **Total reward is negative**
- AI making poor decisions
- Consider retraining with more timesteps

---

## Troubleshooting

### Issue: "Model not found" Error

**Solution:**
```bash
python train.py
```
Wait for training to complete (5-10 minutes)

### Issue: Window doesn't open

**Solution:**
- Ensure pygame is installed: `pip install pygame`
- Check your display settings
- Try running in a different terminal

### Issue: Simulation runs too fast/slow

**Workaround:**
- AI makes decisions every 30 frames (~0.5 seconds at 60 FPS)
- Code is optimized for 60 FPS
- If running slow, check system performance

### Issue: Graphics look weird

**Solution:**
- Ensure pygame is latest version: `pip install --upgrade pygame`
- Check screen resolution (simulator works best at 1200x700 or higher)

---

## Tips for Best Experience

### 1. Start Fresh
```bash
python train.py  # Train with good parameters
python room_simulator.py  # Then simulate
```

### 2. Let It Run
- Give the simulation at least 50-100 steps
- Watch for patterns in AI behavior
- Look for comfort trends over time

### 3. Compare Modes
- Switch between AUTO and MANUAL
- See if you can beat the AI's score
- Learn what strategies work best

### 4. Use Pause Strategically
- Press SPACE to pause
- Examine current state carefully
- Think about what action you'd take
- Resume to see what AI chooses

### 5. Reset Often
- Press R to start fresh simulations
- Test different scenarios
- Check consistency of AI decisions

---

## Advanced Usage

### Modify Simulation Speed

Edit `room_simulator.py`:
```python
if frame_count % 30 == 0:  # Change 30 to faster (15) or slower (60)
    action, _ = self.model.predict(self.obs, deterministic=True)
```

### Add More Metrics

You can modify the status panel to show additional information by editing the `draw_status_panel` method.

### Change Room Appearance

Modify colors and sizes in the `draw_room` method to customize the visual appearance.

---

## Alternative Simulations

### For Web-Based Simulation

Use the Streamlit dashboard instead:
```bash
streamlit run dashboard.py
```

Features:
- Web interface (browser-based)
- Interactive charts with Plotly
- Step-by-step controls
- History tracking

### For Dynamic Environment

Use the dynamic environment simulator:
```bash
python -c "from dynamic_environment import DynamicSmartHomeEnv; env = DynamicSmartHomeEnv()"
```

Features:
- Realistic day/night cycles
- Occupancy variations
- Weather effects
- More complex simulation

---

## What to Look For

### Signs of Good Training

1. **Quick Response to Changes**
   - AI turns fan on within 1-2 steps when hot
   - AI adjusts lights based on time/needs

2. **Comfort Maintenance**
   - Comfort score mostly green
   - Rarely drops below 0.6

3. **Energy Efficiency**
   - Fan not always on
   - Lights adjust based on natural light

4. **Reward Growth**
   - Total reward increasing over time
   - Positive by 20+ steps

### Signs of Poor Training

1. **Random Behavior**
   - Actions don't match conditions
   - No pattern to decisions

2. **Comfort Ignored**
   - Comfort in red frequently
   - Person icon always unhappy

3. **Energy Waste**
   - Fan always on even when cool
   - Lights at max constantly

4. **Negative Rewards**
   - Total reward decreasing
   - Large negative values

---

## Summary

The Room Simulator is a powerful tool to:
- ✅ **Visualize** your AI model in action
- ✅ **Verify** the model makes sensible decisions
- ✅ **Test** different scenarios and conditions
- ✅ **Compare** AI performance vs manual control
- ✅ **Debug** issues with model training

Use it alongside `verify_model.py` and `test_agent.py` for comprehensive model validation!

---

## Quick Reference Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Train model
python train.py

# Run room simulator
python room_simulator.py

# Alternative: Web dashboard
streamlit run dashboard.py

# Verify model
python verify_model.py

# Test agent
python test_agent.py
```

---

Enjoy watching your Smart Home AI in action! 🏠🤖✨
