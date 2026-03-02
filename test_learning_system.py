"""
Test the AI Learning System with Manual Overrides
Demonstrates how the system learns from user preferences
"""
import os
from langgraph_agent import (
    add_manual_override,
    get_ai_recommendation,
    get_memory_stats,
    load_user_memory
)

def test_learning_progression():
    """Test how AI learns from repeated user overrides"""
    
    print("🧪 Testing AI Learning System\n")
    print("=" * 60)
    
    # Clean slate - remove old memory if exists
    if os.path.exists("user_override_memory.json"):
        os.remove("user_override_memory.json")
        print("✅ Cleared previous memory for fresh test\n")
    
    # Initial state - room is getting warm
    warm_room_state = {
        "temperature": 27.5,
        "humidity": 65,
        "occupancy": 1,
        "time_of_day": 14,  # 2 PM
        "hvac_status": 0,   # HVAC OFF
        "lighting": 75,
        "energy_usage": 1.5
    }
    
    print("🏠 Initial Room State:")
    print(f"   Temperature: {warm_room_state['temperature']}°C (Warm!)")
    print(f"   Time: {warm_room_state['time_of_day']}:00")
    print(f"   HVAC: {'ON' if warm_room_state['hvac_status'] else 'OFF'}")
    print(f"   Occupancy: Present\n")
    
    # Step 1: Get AI recommendation BEFORE any learning
    print("📊 STEP 1: AI Recommendation (No Learning Yet)")
    print("-" * 60)
    result_before = get_ai_recommendation(warm_room_state)
    print(f"💡 Recommendation: {result_before['recommendation']}")
    print(f"🧠 Reasoning: {result_before['reasoning']}")
    print(f"📚 Memories Used: {result_before['relevant_overrides']}/{result_before['memory_count']}\n")
    
    # Step 2: Simulate user ALWAYS turning on HVAC when it's 27°C+
    print("📊 STEP 2: Simulating User Learning Pattern")
    print("-" * 60)
    print("User manually turns HVAC ON when temperature reaches 27°C...")
    
    for i in range(5):
        # Slightly vary the conditions to make it realistic
        test_state = warm_room_state.copy()
        test_state["temperature"] = 27.0 + (i * 0.3)  # 27.0 - 28.2°C
        test_state["time_of_day"] = 13 + i  # 1 PM - 5 PM
        
        add_manual_override(test_state, 1, "❄️ Turn HVAC On")
        print(f"   Override {i+1}: Turned HVAC ON at {test_state['temperature']:.1f}°C, {test_state['time_of_day']}:00")
    
    stats = get_memory_stats()
    print(f"\n✅ Recorded {stats['total_overrides']} overrides")
    print(f"   Most common action: {stats['most_common_action']}\n")
    
    # Step 3: Get AI recommendation AFTER learning
    print("📊 STEP 3: AI Recommendation (After Learning)")
    print("-" * 60)
    result_after = get_ai_recommendation(warm_room_state)
    print(f"💡 Recommendation: {result_after['recommendation']}")
    print(f"🧠 Reasoning: {result_after['reasoning']}")
    print(f"📚 Memories Used: {result_after['relevant_overrides']}/{result_after['memory_count']}\n")
    
    # Step 4: Test with DIFFERENT scenario (cooler room)
    cool_room_state = {
        "temperature": 22.0,
        "humidity": 55,
        "occupancy": 1,
        "time_of_day": 14,
        "hvac_status": 1,  # HVAC ON
        "lighting": 75,
        "energy_usage": 3.5
    }
    
    print("📊 STEP 4: Testing Different Scenario (Cool Room)")
    print("-" * 60)
    print(f"🏠 Temperature: {cool_room_state['temperature']}°C (Comfortable)")
    print(f"   HVAC: Currently ON")
    print(f"   Should AI learn that user only wants HVAC when warm?\n")
    
    result_cool = get_ai_recommendation(cool_room_state)
    print(f"💡 Recommendation: {result_cool['recommendation']}")
    print(f"🧠 Reasoning: {result_cool['reasoning']}")
    print(f"📚 Memories Used: {result_cool['relevant_overrides']}/{result_cool['memory_count']}\n")
    
    # Step 5: Evening lighting preference test
    print("📊 STEP 5: Teaching Evening Lighting Preference")
    print("-" * 60)
    print("User dims lights every evening at 10 PM...")
    
    for i in range(3):
        evening_state = {
            "temperature": 23.0,
            "humidity": 58,
            "occupancy": 1,
            "time_of_day": 22,  # 10 PM
            "hvac_status": 0,
            "lighting": 80 - (i * 5),  # Varying starting brightness
            "energy_usage": 2.0
        }
        add_manual_override(evening_state, 4, "🌙 Decrease Lighting")
        print(f"   Override {i+1}: Decreased lighting at 22:00")
    
    stats = get_memory_stats()
    print(f"\n✅ Total memories: {stats['total_overrides']}\n")
    
    # Test evening recommendation
    evening_test = {
        "temperature": 23.0,
        "humidity": 60,
        "occupancy": 1,
        "time_of_day": 22,
        "hvac_status": 0,
        "lighting": 75,
        "energy_usage": 2.0
    }
    
    print("📊 STEP 6: Evening Recommendation (With Lighting Memory)")
    print("-" * 60)
    result_evening = get_ai_recommendation(evening_test)
    print(f"💡 Recommendation: {result_evening['recommendation']}")
    print(f"🧠 Reasoning: {result_evening['reasoning']}")
    print(f"📚 Memories Used: {result_evening['relevant_overrides']}/{result_evening['memory_count']}\n")
    
    # Summary
    print("=" * 60)
    print("🎉 LEARNING TEST COMPLETE!")
    print("=" * 60)
    print("\n📊 Final Statistics:")
    final_stats = get_memory_stats()
    print(f"   Total Overrides Stored: {final_stats['total_overrides']}")
    print(f"   Most Common Action: {final_stats['most_common_action']}")
    print(f"   Status: {final_stats['learning_status']}")
    print("\n✅ The AI is now personalized to user preferences!")
    print("   Check 'user_override_memory.json' to see stored memories.\n")

if __name__ == "__main__":
    test_learning_progression()
