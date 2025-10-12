"""
🤖 PROOF OF CONCEPT: Agentic AI Layer for Smart Home

This demonstrates how LangGraph can add intelligence on top of your existing RL model.

Features demonstrated:
1. Natural language command understanding
2. Context-aware decision making
3. Explanation generation
4. Multi-step planning (basic)
5. Integration with existing RL model

NOTE: This is a MINIMAL implementation to show the concept.
Full implementation would be much more sophisticated.

SETUP: Can run in two modes:
1. DEMO MODE (default) - No dependencies, mock responses
2. FULL MODE - Requires: pip install -r requirements_agentic.txt
"""

import os
from datetime import datetime, timedelta
from typing import TypedDict, List

# Check if full dependencies available
try:
    from langchain_openai import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema.output_parser import StrOutputParser
    from langgraph.graph import StateGraph, END
    FULL_MODE = True
    print("✅ Full mode: LangGraph dependencies found")
except ImportError:
    FULL_MODE = False
    print("ℹ️  Demo mode: Running with mock responses (no dependencies needed)")
    print("   For full mode: pip install -r requirements_agentic.txt\n")

# Check for existing RL model
try:
    from stable_baselines3 import DQN
    RL_MODEL_AVAILABLE = True
except ImportError:
    RL_MODEL_AVAILABLE = False
    print("⚠️  RL model package not available, will use mock actions")

# ============================================================================
# SETUP
# ============================================================================

# Check for API key (only if in full mode)
if FULL_MODE and not os.getenv("OPENAI_API_KEY"):
    print("⚠️  WARNING: No OPENAI_API_KEY found")
    print("   Switching to demo mode with mock responses\n")
    USE_REAL_LLM = False
elif FULL_MODE:
    USE_REAL_LLM = True
    print("✅ OpenAI API key found - using real LLM\n")
else:
    USE_REAL_LLM = False

# ============================================================================
# STATE DEFINITION
# ============================================================================

class AgenticState(TypedDict):
    """State passed between agents"""
    # Input
    user_command: str
    environment_data: dict
    user_context: dict
    
    # Processing
    parsed_intent: dict
    planned_actions: List[dict]
    rl_action: int
    
    # Output
    explanation: str
    confidence: float


# ============================================================================
# AGENT 1: NATURAL LANGUAGE UNDERSTANDING
# ============================================================================

def understand_command(state: AgenticState) -> AgenticState:
    """Parse user's natural language command into structured intent"""
    
    if USE_REAL_LLM and FULL_MODE:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        
        prompt = ChatPromptTemplate.from_template("""
        Parse this smart home command into JSON format.
        
        User said: "{command}"
        Current conditions:
        - Temperature: {temp}°C
        - Light: {light} lux
        - Fan: {fan_status}
        
        Extract:
        - intent: (cooling, heating, lighting_up, lighting_down, maintain, query)
        - urgency: (low, medium, high)
        - constraints: any limitations mentioned
        - temporal: any time-based requirements
        
        Respond ONLY with valid JSON.
        
        Example:
        {{"intent": "cooling", "urgency": "high", "constraints": ["not too cold"], "temporal": null}}
        """)
        
        chain = prompt | llm | StrOutputParser()
        
        response = chain.invoke({
            "command": state["user_command"],
            "temp": state["environment_data"]["temp"],
            "light": state["environment_data"]["light"],
            "fan_status": "ON" if state["environment_data"]["fan"] else "OFF"
        })
        
        # Parse JSON response
        import json
        intent = json.loads(response)
    else:
        # Mock response for demo
        cmd = state["user_command"].lower()
        if "hot" in cmd or "cool" in cmd:
            intent = {"intent": "cooling", "urgency": "high", "constraints": [], "temporal": None}
        elif "cold" in cmd or "warm" in cmd:
            intent = {"intent": "heating", "urgency": "medium", "constraints": [], "temporal": None}
        elif "bright" in cmd or "light" in cmd:
            intent = {"intent": "lighting_down", "urgency": "low", "constraints": [], "temporal": None}
        else:
            intent = {"intent": "maintain", "urgency": "low", "constraints": [], "temporal": None}
    
    state["parsed_intent"] = intent
    print(f"📝 NLU Agent: Parsed intent = {intent['intent']} (urgency: {intent['urgency']})")
    return state


# ============================================================================
# AGENT 2: CONTEXT & MEMORY (Simplified)
# ============================================================================

def load_user_context(state: AgenticState) -> AgenticState:
    """Load user preferences and history"""
    
    # In real implementation, this would query a vector database
    # For now, use simple rules based on time of day
    
    current_hour = datetime.now().hour
    
    # Simulate user preferences
    if 22 <= current_hour or current_hour < 6:
        context = {
            "activity": "sleeping",
            "preferred_temp": 22.0,
            "preferred_light": 0,
            "energy_priority": 0.8  # High priority on quiet/comfort
        }
    elif 6 <= current_hour < 9:
        context = {
            "activity": "waking_up",
            "preferred_temp": 23.0,
            "preferred_light": 400,
            "energy_priority": 0.5
        }
    elif 9 <= current_hour < 17:
        context = {
            "activity": "working",
            "preferred_temp": 24.0,
            "preferred_light": 600,
            "energy_priority": 0.3  # Low priority, comfort matters
        }
    else:
        context = {
            "activity": "relaxing",
            "preferred_temp": 23.0,
            "preferred_light": 300,
            "energy_priority": 0.6
        }
    
    state["user_context"] = context
    print(f"🧠 Context Agent: Current activity = {context['activity']}")
    return state


# ============================================================================
# AGENT 3: PLANNING & REASONING
# ============================================================================

def plan_actions(state: AgenticState) -> AgenticState:
    """Create action plan based on intent and context"""
    
    intent = state["parsed_intent"]
    context = state["user_context"]
    env = state["environment_data"]
    
    # Simple rule-based planning (in real system, would use LLM reasoning)
    planned_actions = []
    
    if intent["intent"] == "cooling":
        if env["temp"] > context["preferred_temp"] + 2:
            planned_actions.append({
                "type": "immediate",
                "action": 1,  # Fan ON
                "reason": "Temperature significantly above preference"
            })
        elif env["temp"] > context["preferred_temp"]:
            planned_actions.append({
                "type": "immediate",
                "action": 1,  # Fan ON
                "reason": "Gradual cooling needed"
            })
    
    elif intent["intent"] == "heating":
        if env["fan"]:
            planned_actions.append({
                "type": "immediate",
                "action": 2,  # Fan OFF
                "reason": "Stop cooling to allow warming"
            })
    
    elif intent["intent"] == "lighting_up":
        if env["light"] < context["preferred_light"]:
            planned_actions.append({
                "type": "immediate",
                "action": 3,  # Light up
                "reason": "Increase brightness for activity"
            })
    
    elif intent["intent"] == "lighting_down":
        if env["light"] > context["preferred_light"]:
            planned_actions.append({
                "type": "immediate",
                "action": 4,  # Light down
                "reason": "Reduce brightness"
            })
    
    else:  # maintain
        planned_actions.append({
            "type": "immediate",
            "action": 0,  # Do nothing
            "reason": "Conditions are acceptable"
        })
    
    # Add temporal planning if user mentioned time
    if intent.get("temporal"):
        # Would add scheduled actions here
        pass
    
    state["planned_actions"] = planned_actions
    
    if planned_actions:
        print(f"📋 Planning Agent: {len(planned_actions)} actions planned")
        for i, action in enumerate(planned_actions):
            print(f"   {i+1}. Action {action['action']}: {action['reason']}")
    
    return state


# ============================================================================
# AGENT 4: RL EXECUTION (Your existing model)
# ============================================================================

def execute_with_rl(state: AgenticState) -> AgenticState:
    """Use RL model to execute action (or validate planned action)"""
    
    if RL_MODEL_AVAILABLE:
        try:
            # Load your trained RL model
            model = DQN.load("smart_home_ai_brain.zip")
            
            # Get RL's recommendation
            obs = [
                state["environment_data"]["temp"],
                state["environment_data"]["temp"],  # perceived temp (simplified)
                state["environment_data"]["light"],
                state["environment_data"]["comfort"],
                1 if state["environment_data"]["fan"] else 0,
                state["environment_data"]["light_percent"],
                state["environment_data"]["energy"]
            ]
            
            rl_action, _ = model.predict(obs, deterministic=True)
            rl_action = int(rl_action)
            
            # Compare RL suggestion with planned action
            if state["planned_actions"]:
                planned_action = state["planned_actions"][0]["action"]
                
                if rl_action == planned_action:
                    state["rl_action"] = rl_action
                    state["confidence"] = 0.95
                    print(f"🤖 RL Agent: Agrees with plan (Action {rl_action})")
                else:
                    # RL disagrees - use RL's expertise for numerical optimization
                    state["rl_action"] = rl_action
                    state["confidence"] = 0.75
                    print(f"⚠️  RL Agent: Suggests different action {rl_action} (planned: {planned_action})")
            else:
                state["rl_action"] = rl_action
                state["confidence"] = 0.80
                print(f"🤖 RL Agent: Recommends Action {rl_action}")
            
        except FileNotFoundError:
            print("⚠️  RL model not found, using planned action")
            if state["planned_actions"]:
                state["rl_action"] = state["planned_actions"][0]["action"]
                state["confidence"] = 0.60
            else:
                state["rl_action"] = 0  # Default to do nothing
                state["confidence"] = 0.50
    else:
        # No RL package, use planned action
        print("🤖 RL Agent (simulated): Using planned action")
        if state["planned_actions"]:
            state["rl_action"] = state["planned_actions"][0]["action"]
            state["confidence"] = 0.75
        else:
            state["rl_action"] = 0
            state["confidence"] = 0.60
    
    return state


# ============================================================================
# AGENT 5: EXPLANATION GENERATION
# ============================================================================

def generate_explanation(state: AgenticState) -> AgenticState:
    """Generate human-friendly explanation of decision"""
    
    action_names = {
        0: "maintain current conditions",
        1: "turn the fan ON to cool the room",
        2: "turn the fan OFF",
        3: "increase lighting brightness",
        4: "decrease lighting brightness"
    }
    
    action_name = action_names.get(state["rl_action"], "take an action")
    intent = state["parsed_intent"]["intent"]
    context = state["user_context"]
    env = state["environment_data"]
    
    # Build explanation
    explanation_parts = []
    
    # What we're doing
    explanation_parts.append(f"I'm going to {action_name}.")
    
    # Why (based on intent)
    if intent == "cooling":
        explanation_parts.append(
            f"You mentioned feeling hot, and the current temperature is {env['temp']:.1f}°C, "
            f"which is above your preferred {context['preferred_temp']:.1f}°C for {context['activity']}."
        )
    elif intent == "heating":
        explanation_parts.append(
            f"You mentioned feeling cold. I'll help warm up the room."
        )
    elif intent in ["lighting_up", "lighting_down"]:
        explanation_parts.append(
            f"I'll adjust the lighting to better suit your {context['activity']} activity."
        )
    else:
        explanation_parts.append(
            f"Current conditions are good for {context['activity']}."
        )
    
    # Confidence
    if state["confidence"] > 0.9:
        explanation_parts.append("I'm very confident this is the right choice.")
    elif state["confidence"] > 0.7:
        explanation_parts.append("This should help improve your comfort.")
    else:
        explanation_parts.append("Let me know if you'd like me to adjust differently.")
    
    state["explanation"] = " ".join(explanation_parts)
    print(f"💬 Explanation Agent: Generated response")
    
    return state


# ============================================================================
# BUILD LANGGRAPH WORKFLOW (or simple sequential for demo)
# ============================================================================

def create_agentic_workflow():
    """Build the multi-agent workflow"""
    
    if FULL_MODE:
        workflow = StateGraph(AgenticState)
        
        # Add agent nodes
        workflow.add_node("understand", understand_command)
        workflow.add_node("load_context", load_user_context)
        workflow.add_node("plan", plan_actions)
        workflow.add_node("execute", execute_with_rl)
        workflow.add_node("explain", generate_explanation)
        
        # Define flow
        workflow.set_entry_point("understand")
        workflow.add_edge("understand", "load_context")
        workflow.add_edge("load_context", "plan")
        workflow.add_edge("plan", "execute")
        workflow.add_edge("execute", "explain")
        workflow.add_edge("explain", END)
        
        return workflow.compile()
    else:
        # Simple sequential execution for demo mode
        class SimpleWorkflow:
            def invoke(self, state):
                state = understand_command(state)
                state = load_user_context(state)
                state = plan_actions(state)
                state = execute_with_rl(state)
                state = generate_explanation(state)
                return state
        
        return SimpleWorkflow()


# ============================================================================
# DEMO FUNCTION
# ============================================================================

def demo_agentic_control():
    """Demonstrate the agentic AI system"""
    
    print("\n" + "="*70)
    print("🤖 AGENTIC AI SMART HOME - PROOF OF CONCEPT")
    print("="*70)
    print("\nThis demonstrates how LangGraph adds intelligence to your RL model.")
    print("Watch as multiple agents collaborate to understand and execute commands!\n")
    
    # Create workflow
    app = create_agentic_workflow()
    
    # Test scenarios
    scenarios = [
        {
            "command": "I'm too hot, make it cooler",
            "env": {
                "temp": 28.0,
                "light": 450,
                "fan": False,
                "comfort": 0.5,
                "light_percent": 60,
                "energy": 1.2
            }
        },
        {
            "command": "It's too bright in here",
            "env": {
                "temp": 24.0,
                "light": 800,
                "fan": True,
                "comfort": 0.7,
                "light_percent": 80,
                "energy": 2.0
            }
        },
        {
            "command": "Everything is perfect",
            "env": {
                "temp": 23.5,
                "light": 500,
                "fan": False,
                "comfort": 0.8,
                "light_percent": 65,
                "energy": 1.0
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'─'*70}")
        print(f"📋 SCENARIO {i}")
        print(f"{'─'*70}")
        print(f"👤 User: \"{scenario['command']}\"")
        print(f"🌡️  Environment: Temp={scenario['env']['temp']:.1f}°C, "
              f"Light={scenario['env']['light']}lux, "
              f"Fan={'ON' if scenario['env']['fan'] else 'OFF'}")
        print()
        
        # Run workflow
        result = app.invoke({
            "user_command": scenario["command"],
            "environment_data": scenario["env"],
            "user_context": {},
            "parsed_intent": {},
            "planned_actions": [],
            "rl_action": 0,
            "explanation": "",
            "confidence": 0.0
        })
        
        # Display results
        print()
        print("─" * 70)
        print("📊 RESULTS")
        print("─" * 70)
        print(f"🎯 Action Chosen: {result['rl_action']}")
        action_names_display = [
            "Do Nothing",
            "Turn Fan ON",
            "Turn Fan OFF", 
            "Increase Light",
            "Decrease Light"
        ]
        print(f"   ({action_names_display[result['rl_action']]})")
        print(f"📈 Confidence: {result['confidence']*100:.0f}%")
        print(f"\n💬 AI Explanation:")
        print(f"   \"{result['explanation']}\"")
        print()
    
    print("="*70)
    print("✨ DEMO COMPLETE!")
    print("="*70)
    print("\n🎓 What you just saw:")
    print("   • NLU Agent parsed natural language commands")
    print("   • Context Agent loaded user preferences")
    print("   • Planning Agent created action plans")
    print("   • RL Agent executed optimal control")
    print("   • Explanation Agent generated human-friendly responses")
    print("\n💡 This is just the beginning! Full implementation would include:")
    print("   • Multi-step temporal planning")
    print("   • Vector database for long-term memory")
    print("   • Multiple specialized agents")
    print("   • Voice interface integration")
    print("   • Real-time learning from feedback")
    print("\n📖 Read AGENTIC_AI_INTEGRATION.md for full implementation guide!")
    print()


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    demo_agentic_control()
