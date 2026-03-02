"""
Smart Home AI Agent with Persistent Memory
Integrates with Gemini API to provide intelligent home automation decisions
Learns from user manual overrides over time
"""
import os
import json
from datetime import datetime
from typing import TypedDict, List, Dict
import google.generativeai as genai

# Set API key
API_KEY = "AIzaSyC_uWqJJUCIM7OB5FYa9zXYirrD03Gn7io"
genai.configure(api_key=API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Memory storage file
MEMORY_FILE = "user_override_memory.json"

# Define the state
class AgentState(TypedDict):
    current_state: dict
    recommendation: str
    reasoning: str
    analysis: str
    user_memory: list  # Stores past manual overrides

# Memory management functions
def load_user_memory() -> List[Dict]:
    """Load user manual override memory from file"""
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading memory: {e}")
    return []

def save_user_memory(memory: List[Dict]):
    """Save user manual override memory to file"""
    try:
        # Keep only last 100 overrides to prevent file from growing too large
        memory = memory[-100:] if len(memory) > 100 else memory
        with open(MEMORY_FILE, 'w') as f:
            json.dump(memory, f, indent=2)
    except Exception as e:
        print(f"Error saving memory: {e}")

def add_manual_override(environment_state: dict, action_taken: int, action_name: str):
    """
    Record a manual override action by the user
    
    Args:
        environment_state: Current state when user intervened
        action_taken: Action ID (0-4)
        action_name: Human-readable action name
    """
    memory = load_user_memory()
    
    override_record = {
        "timestamp": datetime.now().isoformat(),
        "temperature": environment_state.get("temperature"),
        "humidity": environment_state.get("humidity"),
        "occupancy": environment_state.get("occupancy"),
        "time_of_day": environment_state.get("time_of_day"),
        "hvac_status": environment_state.get("hvac_status"),
        "lighting": environment_state.get("lighting"),
        "energy_usage": environment_state.get("energy_usage"),
        "user_action": action_taken,
        "action_name": action_name
    }
    
    memory.append(override_record)
    save_user_memory(memory)
    print(f"✅ Recorded manual override: {action_name}")

def get_relevant_overrides(current_state: dict, max_examples: int = 5) -> List[Dict]:
    """
    Get relevant past overrides similar to current state
    
    Args:
        current_state: Current environment state
        max_examples: Maximum number of examples to return
        
    Returns:
        List of relevant override records
    """
    memory = load_user_memory()
    if not memory:
        return []
    
    # Simple relevance: find overrides in similar temperature and time ranges
    current_temp = current_state.get("temperature", 22)
    current_time = current_state.get("time_of_day", 12)
    
    relevant = []
    for record in memory:
        temp_diff = abs(record.get("temperature", 22) - current_temp)
        time_diff = abs(record.get("time_of_day", 12) - current_time)
        
        # Consider relevant if within 3°C and 3 hours
        if temp_diff <= 3 and time_diff <= 3:
            relevant.append(record)
    
    # Return most recent relevant examples
    return relevant[-max_examples:] if relevant else memory[-max_examples:]

def format_memory_context(overrides: List[Dict]) -> str:
    """Format user override history for Gemini prompt"""
    if not overrides:
        return "No previous user preferences recorded."
    
    context = "User's past manual interventions (most recent):\n"
    for i, override in enumerate(overrides, 1):
        context += f"\n{i}. {override.get('action_name', 'Unknown')} when:"
        context += f"\n   - Temp: {override.get('temperature')}°C"
        context += f"\n   - Time: {override.get('time_of_day')}:00"
        context += f"\n   - HVAC was: {'On' if override.get('hvac_status') else 'Off'}"
        context += f"\n   - Lighting: {override.get('lighting')}%"
    
    return context

# Node functions
def analyze_environment(state: AgentState) -> AgentState:
    """Analyze current smart home environment state with user preference context"""
    current = state.get("current_state", {})
    user_memory = state.get("user_memory", [])
    
    memory_context = format_memory_context(user_memory)
    
    prompt = f"""
    You are an AI agent managing a smart home for a SINGLE PERSON living alone. 
    Analyze this current state:
    
    🏠 Current State:
    Temperature: {current.get('temperature', 'N/A')}°C
    Humidity: {current.get('humidity', 'N/A')}%
    Occupancy: {'Yes - Person is home' if current.get('occupancy', 0) > 0 else 'No - Person is away'}
    Time of Day: {current.get('time_of_day', 'N/A')}:00
    HVAC Status: {'On' if current.get('hvac_status', 0) == 1 else 'Off'}
    Lighting: {current.get('lighting', 'N/A')}%
    Energy Usage: {current.get('energy_usage', 'N/A')} kWh
    
    👤 User Preference History:
    {memory_context}
    
    IMPORTANT: Consider the user's past manual interventions. If they have consistently 
    overridden the system in similar situations, learn from their preferences!
    
    Provide a brief analysis in 2-3 sentences, mentioning any relevant user patterns.
    """
    
    response = model.generate_content(prompt)
    state["analysis"] = response.text
    
    return state

def make_recommendation(state: AgentState) -> AgentState:
    """Generate smart home action recommendations based on learning from user"""
    current = state.get("current_state", {})
    analysis = state.get("analysis", "")
    user_memory = state.get("user_memory", [])
    
    memory_context = format_memory_context(user_memory)
    
    prompt = f"""
    Based on this analysis: {analysis}
    
    🏠 Current state:
    - Temperature: {current.get('temperature', 'N/A')}°C
    - Humidity: {current.get('humidity', 'N/A')}%
    - Occupancy: {'Yes - Person is home' if current.get('occupancy', 0) > 0 else 'No - Person is away'}
    - Time: {current.get('time_of_day', 'N/A')}:00
    - HVAC: {'On' if current.get('hvac_status', 0) == 1 else 'Off'}
    - Lighting: {current.get('lighting', 'N/A')}%
    
    👤 User's Historical Preferences:
    {memory_context}
    
    CRITICAL: This system is learning from the user's manual overrides. 
    - If the user has manually intervened in similar conditions, PRIORITIZE their preference!
    - The goal is to predict what the user would do themselves.
    - Balance comfort, energy efficiency, AND user habits.
    
    Available actions:
    1. Turn HVAC On
    2. Turn HVAC Off  
    3. Increase Lighting
    4. Decrease Lighting
    5. Do Nothing (maintain current state)
    
    Respond with ONLY the specific action name (e.g., "Turn HVAC On", "Decrease Lighting", "Do Nothing").
    Choose the action the USER would most likely prefer based on their history.
    """
    
    response = model.generate_content(prompt)
    state["recommendation"] = response.text.strip()
    
    return state

def explain_decision(state: AgentState) -> AgentState:
    """Explain the reasoning behind the recommendation with user context"""
    current = state.get("current_state", {})
    recommendation = state.get("recommendation", "")
    user_memory = state.get("user_memory", [])
    
    has_memory = len(user_memory) > 0
    
    prompt = f"""
    You recommended: {recommendation}
    
    User has {'learned preferences' if has_memory else 'no recorded preferences yet'}.
    
    Explain WHY this is the best action in 2-3 sentences, considering:
    - The user's past manual interventions {('(' + str(len(user_memory)) + ' recorded)') if has_memory else ''}
    - Energy efficiency
    - Comfort optimization for a single person
    - Current conditions
    
    {'Start with: "Based on your preferences..." if the recommendation aligns with past overrides.' if has_memory else ''}
    
    Be concise, personal, and practical.
    """
    
    response = model.generate_content(prompt)
    state["reasoning"] = response.text
    
    return state

def get_ai_recommendation(environment_state: dict) -> dict:
    """
    Get AI recommendation for smart home actions with user learning
    
    Args:
        environment_state: Dictionary with current home state
        
    Returns:
        Dictionary with recommendation, reasoning, and memory stats
    """
    # Load relevant user memory
    user_memory = get_relevant_overrides(environment_state)
    
    # Create initial state
    state = {
        "current_state": environment_state,
        "recommendation": "",
        "reasoning": "",
        "analysis": "",
        "user_memory": user_memory
    }
    
    # Run the workflow manually (without LangGraph)
    state = analyze_environment(state)
    state = make_recommendation(state)
    state = explain_decision(state)
    
    return {
        "recommendation": state["recommendation"],
        "reasoning": state["reasoning"],
        "analysis": state["analysis"],
        "memory_count": len(load_user_memory()),
        "relevant_overrides": len(user_memory)
    }

def chat_with_agent(user_message: str, environment_state: dict) -> str:
    """
    Chat with the AI agent about smart home with memory context
    
    Args:
        user_message: User's question or command
        environment_state: Current home state
        
    Returns:
        AI response
    """
    user_memory = load_user_memory()
    memory_summary = f"\n\nI have learned from {len(user_memory)} of your manual adjustments." if user_memory else ""
    
    prompt = f"""
    You are a smart home AI assistant for a SINGLE PERSON living alone. 
    Current home state:
    
    Temperature: {environment_state.get('temperature', 'N/A')}°C
    Humidity: {environment_state.get('humidity', 'N/A')}%
    Occupancy: {'Yes - You are home' if environment_state.get('occupancy', 0) > 0 else 'No - You are away'}
    HVAC: {'On' if environment_state.get('hvac_status', 0) == 1 else 'Off'}
    Lighting: {environment_state.get('lighting', 'N/A')}%
    Energy Usage: {environment_state.get('energy_usage', 'N/A')} kWh{memory_summary}
    
    User says: {user_message}
    
    Respond helpfully and personally (2-3 sentences max). You're learning their preferences over time.
    """
    
    response = model.generate_content(prompt)
    return response.text

def get_memory_stats() -> dict:
    """Get statistics about stored user preferences"""
    memory = load_user_memory()
    
    if not memory:
        return {
            "total_overrides": 0,
            "most_common_action": "None",
            "learning_status": "No data yet - start using manual controls!",
            "patterns": []
        }
    
    # Count action frequencies
    action_counts = {}
    for record in memory:
        action = record.get("action_name", "Unknown")
        action_counts[action] = action_counts.get(action, 0) + 1
    
    most_common = max(action_counts.items(), key=lambda x: x[1]) if action_counts else ("None", 0)
    
    # Detect confident patterns
    patterns = detect_confident_patterns(memory)
    
    return {
        "total_overrides": len(memory),
        "most_common_action": most_common[0],
        "action_frequency": most_common[1],
        "learning_status": f"Active learning from {len(memory)} interactions",
        "patterns": patterns
    }

def detect_confident_patterns(memory: List[Dict], confidence_threshold: int = 3) -> List[Dict]:
    """
    Detect patterns where user consistently does the same action
    in similar conditions (confident patterns)
    
    Args:
        memory: List of override records
        confidence_threshold: Minimum occurrences to be confident
        
    Returns:
        List of detected patterns with confidence levels
    """
    patterns = []
    
    # Group by action type
    action_groups = {}
    for record in memory:
        action = record.get("user_action")
        if action not in action_groups:
            action_groups[action] = []
        action_groups[action].append(record)
    
    # Analyze each action group for patterns
    for action_id, records in action_groups.items():
        if len(records) < confidence_threshold:
            continue
        
        # Temperature-based patterns (for HVAC)
        if action_id in [1, 2]:  # HVAC actions
            temps = [r.get("temperature", 0) for r in records]
            avg_temp = sum(temps) / len(temps)
            temp_range = (min(temps), max(temps))
            
            patterns.append({
                "action_id": action_id,
                "action_name": records[0].get("action_name", "Unknown"),
                "trigger": "temperature",
                "condition": f"{avg_temp:.1f}°C (range: {temp_range[0]:.1f}-{temp_range[1]:.1f}°C)",
                "occurrences": len(records),
                "confidence": min(100, (len(records) / confidence_threshold) * 100),
                "recommendation": f"Auto-apply when temp ≈ {avg_temp:.1f}°C"
            })
        
        # Time-based patterns (for lighting)
        elif action_id in [3, 4]:  # Lighting actions
            times = [r.get("time_of_day", 12) for r in records]
            avg_time = int(sum(times) / len(times))
            time_range = (min(times), max(times))
            
            patterns.append({
                "action_id": action_id,
                "action_name": records[0].get("action_name", "Unknown"),
                "trigger": "time_of_day",
                "condition": f"{avg_time:02d}:00 (range: {time_range[0]:02d}:00-{time_range[1]:02d}:00)",
                "occurrences": len(records),
                "confidence": min(100, (len(records) / confidence_threshold) * 100),
                "recommendation": f"Auto-apply around {avg_time:02d}:00"
            })
    
    # Sort by confidence (highest first)
    patterns.sort(key=lambda x: x["confidence"], reverse=True)
    
    return patterns

def should_auto_apply(current_state: dict, confidence_threshold: int = 5) -> dict:
    """
    Check if we should automatically apply a learned pattern
    
    Args:
        current_state: Current environment state
        confidence_threshold: Minimum overrides needed for auto-apply
        
    Returns:
        Dict with auto_apply recommendation or None
    """
    memory = load_user_memory()
    patterns = detect_confident_patterns(memory, confidence_threshold)
    
    current_temp = current_state.get("temperature", 22)
    current_time = current_state.get("time_of_day", 12)
    
    for pattern in patterns:
        # High confidence pattern (5+ occurrences)
        if pattern["confidence"] >= 100:
            
            # Temperature-based pattern matching
            if pattern["trigger"] == "temperature":
                # Extract average temp from condition string
                avg_temp = float(pattern["condition"].split("°C")[0])
                if abs(current_temp - avg_temp) <= 2:  # Within 2°C
                    return {
                        "should_apply": True,
                        "action_id": pattern["action_id"],
                        "action_name": pattern["action_name"],
                        "reason": f"You've done this {pattern['occurrences']} times at ~{avg_temp:.1f}°C",
                        "confidence": pattern["confidence"]
                    }
            
            # Time-based pattern matching
            elif pattern["trigger"] == "time_of_day":
                # Extract average time from condition string
                avg_time = int(pattern["condition"].split(":")[0])
                if abs(current_time - avg_time) <= 1:  # Within 1 hour
                    return {
                        "should_apply": True,
                        "action_id": pattern["action_id"],
                        "action_name": pattern["action_name"],
                        "reason": f"You've done this {pattern['occurrences']} times around {avg_time:02d}:00",
                        "confidence": pattern["confidence"]
                    }
    
    return {"should_apply": False}

if __name__ == "__main__":
    # Test the agent
    test_state = {
        "temperature": 28,
        "humidity": 65,
        "occupancy": 1,
        "time_of_day": 14,
        "hvac_status": 0,
        "lighting": 75,
        "energy_usage": 2.5
    }
    
    print("🤖 Testing Smart Home AI Agent...\n")
    result = get_ai_recommendation(test_state)
    
    print(f"📊 Analysis: {result['analysis']}\n")
    print(f"💡 Recommendation: {result['recommendation']}\n")
    print(f"🧠 Reasoning: {result['reasoning']}\n")
