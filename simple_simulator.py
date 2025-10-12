"""
Simple Console-Based Room Simulator
====================================
Watch your AI control a room in real-time with simple text output
"""

from stable_baselines3 import DQN
from environment import SmartHomeEnv
import time
import sys
import os

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_comfort_emoji(comfort):
    """Get emoji based on comfort level"""
    if comfort > 0.7:
        return "😊 Very Comfortable"
    elif comfort > 0.5:
        return "😐 Moderately Comfortable"
    else:
        return "😟 Uncomfortable"

def get_temp_indicator(temp):
    """Get visual temperature indicator"""
    if temp < 20:
        return "🥶 COLD"
    elif temp < 23:
        return "❄️  Cool"
    elif temp < 26:
        return "✅ Perfect"
    elif temp < 29:
        return "🌡️  Warm"
    else:
        return "🔥 HOT"

def draw_bar(value, max_value, width=30, char="█"):
    """Draw a simple progress bar"""
    filled = int((value / max_value) * width)
    bar = char * filled + "░" * (width - filled)
    return bar

def main():
    print("\n" + "="*70)
    print("         🏠 SMART HOME AI - SIMPLE SIMULATOR 🏠")
    print("="*70)
    
    # Load model
    try:
        print("\n⏳ Loading AI model...")
        model = DQN.load("smart_home_ai_brain.zip")
        print("✅ Model loaded successfully!\n")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        print("\n💡 Please train the model first:")
        print("   python train.py")
        return
    
    # Create environment
    env = SmartHomeEnv(data_file="SmartHome_Environment_v1.csv")
    obs, _ = env.reset()
    
    # Action names
    action_names = {
        0: "Do Nothing",
        1: "Turn Fan ON",
        2: "Turn Fan OFF",
        3: "Increase Light +20%",
        4: "Decrease Light -20%"
    }
    
    print("🎬 Starting simulation...")
    print("   Press Ctrl+C to stop at any time\n")
    time.sleep(2)
    
    step = 0
    total_reward = 0
    
    try:
        while step < 100:  # Run for 100 steps
            clear_screen()
            
            # Header
            print("\n" + "="*70)
            print(f"         🏠 SMART HOME AI SIMULATOR - STEP {step + 1}/100")
            print("="*70 + "\n")
            
            # Extract current state
            temp = obs[0]
            light = obs[2]
            comfort = obs[3]
            fan_on = bool(obs[4])
            light_percent = obs[5]
            energy = obs[6]
            
            # Display Room Status
            print("📊 ROOM STATUS:")
            print("─" * 70)
            
            # Temperature
            temp_indicator = get_temp_indicator(temp)
            print(f"🌡️  Temperature:  {temp:.1f}°C  {temp_indicator}")
            print(f"    {draw_bar(temp, 40, 40)}")
            
            # Light
            print(f"\n💡 Light Level:   {light:.0f} lux  ({light_percent:.0f}% brightness)")
            print(f"    {draw_bar(light_percent, 100, 40)}")
            
            # Comfort
            comfort_status = get_comfort_emoji(comfort)
            print(f"\n😊 Comfort:       {comfort:.2f}  {comfort_status}")
            print(f"    {draw_bar(comfort, 1.0, 40)}")
            
            # Energy
            print(f"\n⚡ Energy:        {energy:.2f} kW")
            print(f"    {draw_bar(energy, 5.0, 40)}")
            
            # Fan status
            fan_status = "🌀 ON (Cooling)" if fan_on else "⭕ OFF"
            print(f"\n🪭 Fan Status:    {fan_status}")
            
            # AI Decision
            print("\n" + "─" * 70)
            print("🤖 AI DECISION:")
            print("─" * 70)
            
            # Let AI make decision
            action, _ = model.predict(obs, deterministic=True)
            action = int(action)
            
            print(f"\n   Action: {action} - {action_names[action]}")
            
            # Execute action
            obs, reward, terminated, _, _ = env.step(action)
            total_reward += reward
            
            print(f"   Reward: {reward:+.2f}")
            print(f"   Total Reward: {total_reward:+.2f}")
            
            # Performance Summary
            print("\n" + "─" * 70)
            print("📈 PERFORMANCE:")
            print("─" * 70)
            
            if comfort > 0.7:
                print("   ✅ User is comfortable")
            elif comfort > 0.5:
                print("   ⚠️  User comfort could be better")
            else:
                print("   ❌ User is uncomfortable!")
            
            if energy < 2.0:
                print("   ✅ Energy usage is efficient")
            else:
                print("   ⚠️  High energy consumption")
            
            if total_reward > 0:
                print("   ✅ AI is performing well (positive reward)")
            else:
                print("   ⚠️  AI needs improvement (negative reward)")
            
            print("\n" + "="*70)
            print("⏸️  Next update in 1 second... (Press Ctrl+C to stop)")
            print("="*70)
            
            step += 1
            
            if terminated:
                print("\n🏁 Simulation completed! Restarting...")
                obs, _ = env.reset()
                step = 0
                total_reward = 0
                time.sleep(2)
            else:
                time.sleep(1)  # Wait 1 second between steps
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Simulation stopped by user")
    
    # Final summary
    print("\n" + "="*70)
    print("                    📊 FINAL SUMMARY")
    print("="*70)
    print(f"\n   Steps completed: {step}")
    print(f"   Total reward: {total_reward:.2f}")
    print(f"   Average reward per step: {total_reward/max(1, step):.2f}")
    
    if total_reward > 0:
        print("\n   ✅ ✅ ✅  YOUR MODEL IS WORKING WELL! ✅ ✅ ✅")
        print("   The AI successfully balanced comfort and energy efficiency.")
    else:
        print("\n   ⚠️  Model needs improvement")
        print("   Consider training longer: python train.py")
    
    print("\n" + "="*70)
    print("   Thanks for using Smart Home AI Simulator!")
    print("="*70 + "\n")
    
    env.close()

if __name__ == "__main__":
    main()
