# 🧠 AI Learning System - Personalized Smart Home Control

## Overview
This Smart Home AI system now features **persistent learning from user preferences**. The Gemini AI agent remembers every manual override you make and evolves its recommendations to match your personal preferences over time.

---

## 🎯 How It Works

### 1. **Single Person Focus**
- The system is optimized for **ONE person** living alone
- All recommendations are personalized to your individual comfort preferences
- No need to balance multiple users' preferences

### 2. **Manual Override Memory**
When you manually control the home using the dashboard controls, the system records:
- ✅ Current temperature and humidity
- ✅ Time of day (what hour you made the change)
- ✅ HVAC and lighting status before your action
- ✅ Which action you chose
- ✅ Energy usage context

This data is stored in `user_override_memory.json` and persists across sessions.

### 3. **Contextual Learning**
The AI analyzes your past overrides to find patterns:
- **Temperature Preferences**: If you always turn on HVAC at 26°C, it learns you prefer cooler temps
- **Time-Based Habits**: If you dim lights at 10 PM every night, it learns your evening routine
- **Energy vs Comfort**: Learns if you prioritize comfort over energy savings
- **Seasonal Patterns**: Adapts to your preferences in different conditions

### 4. **Intelligent Recommendations**
When providing suggestions, Gemini AI:
1. ✅ Analyzes current environment state
2. ✅ Retrieves relevant past overrides (similar temp, time, conditions)
3. ✅ Predicts what YOU would do in this situation
4. ✅ Explains reasoning based on your learned preferences
5. ✅ Continuously improves accuracy with more data

---

## 🚀 How to Use

### Step 1: Initial Training Period
1. **Run the dashboard**: `streamlit run live_simulation_dashboard.py`
2. **Enable Manual Control** in the sidebar
3. **Make manual adjustments** when the AI doesn't match your preference
4. **The system records every override** with full context

### Step 2: Watch It Learn
- After **5-10 manual overrides**, the AI starts recognizing patterns
- After **20+ overrides**, recommendations become highly personalized
- The "AI Learning Status" panel shows how many memories it has

### Step 3: Observe Evolution
- The AI's recommendations will increasingly match what you would do
- Explanations will reference "Based on your preferences..."
- The system balances your habits with energy efficiency

---

## 📊 Key Components

### LangGraph Agent (`langgraph_agent.py`)
**New Functions:**
- `load_user_memory()` - Loads saved override history
- `save_user_memory()` - Persists overrides to disk
- `add_manual_override()` - Records new user actions
- `get_relevant_overrides()` - Finds similar past situations
- `format_memory_context()` - Prepares history for Gemini

**Enhanced Nodes:**
- `analyze_environment()` - Now includes user preference context
- `make_recommendation()` - Prioritizes learned user habits
- `explain_decision()` - References past overrides in reasoning

### Dashboard (`live_simulation_dashboard.py`)
**New Features:**
- 🎮 Manual override buttons record to memory automatically
- 🧠 AI Learning Status panel shows memory statistics
- 📚 Displays relevant vs total memories in AI analysis
- ✅ Success feedback when AI learns from your action

### Memory Storage (`user_override_memory.json`)
Automatically created file storing:
```json
[
  {
    "timestamp": "2025-11-06T14:30:00",
    "temperature": 27.5,
    "humidity": 65,
    "time_of_day": 14,
    "hvac_status": 0,
    "lighting": 75,
    "user_action": 1,
    "action_name": "Turn HVAC On"
  }
]
```

---

## 🎓 Example Learning Scenarios

### Scenario 1: Temperature Preference
**Initial State:** AI turns HVAC on at 25°C  
**You Override:** Turn HVAC on at 24°C multiple times  
**AI Learns:** You prefer cooler temps → Recommends HVAC at 24°C going forward

### Scenario 2: Evening Routine  
**Initial State:** AI keeps lights at 80% at 10 PM  
**You Override:** Reduce lighting to 30% at 10 PM consistently  
**AI Learns:** You prefer dim lighting in evening → Recommends lower lighting at that time

### Scenario 3: Energy vs Comfort
**Initial State:** AI suggests turning off HVAC to save energy  
**You Override:** Keep HVAC on despite energy cost  
**AI Learns:** Comfort is your priority → Adjusts energy/comfort balance

---

## 🔧 Technical Details

### Memory Management
- **Storage**: JSON file in project directory
- **Capacity**: Last 100 overrides (prevents file bloat)
- **Relevance**: Filters by ±3°C temperature and ±3 hours time similarity
- **Persistence**: Survives application restarts

### Gemini Integration
- **API**: Google Gemini 2.0 Flash model
- **Context Window**: Passes up to 5 most relevant overrides per query
- **Prompting**: Explicitly instructs model to prioritize user patterns
- **Learning**: Uses few-shot learning from override examples

### DQN Model
- **Role**: Still provides baseline automation
- **Independence**: Operates separately from LangGraph
- **Use Case**: Runs continuous simulation while you observe
- **Override**: Manual controls override DQN decisions

---

## 📈 Monitoring Your AI's Learning

### Dashboard Indicators
1. **Learning From X overrides** - Total memories stored
2. **Most Common Action** - Your most frequent manual intervention
3. **Relevant Now** - How many past overrides match current situation
4. **Reasoning Text** - Look for "Based on your preferences..." phrases

### Memory Statistics
Access via code:
```python
from langgraph_agent import get_memory_stats

stats = get_memory_stats()
print(f"Total overrides: {stats['total_overrides']}")
print(f"Most common: {stats['most_common_action']}")
```

---

## 🎯 Best Practices

### For Best Learning Results:
1. ✅ **Be Consistent**: Override in similar situations the same way
2. ✅ **Use Manual Mode**: When teaching new preferences
3. ✅ **Review AI Reasoning**: Check if it's learning correctly
4. ✅ **Give It Time**: 20+ overrides for strong patterns
5. ✅ **Vary Conditions**: Override in different times/temps so AI learns full range

### What to Override:
- When AI action doesn't match your comfort preference
- When you have a specific routine (morning, evening, etc.)
- When you prioritize differently (comfort vs energy)
- When external factors matter (guests, weather, etc.)

---

## 🔐 Privacy & Data

### What's Stored:
- Environmental sensor data (temp, humidity)
- Device states (HVAC, lights)
- Your action choices
- Timestamps

### What's NOT Stored:
- No personal information
- No camera/audio data
- No location data
- Only stored locally on your machine

### Data Location:
- File: `user_override_memory.json` in project folder
- Delete file anytime to reset learning
- No cloud upload (unless you configure it)

---

## 🛠️ Advanced Configuration

### Adjust Memory Relevance:
Edit `langgraph_agent.py`:
```python
# Change similarity thresholds
temp_diff <= 3  # ±3°C (adjust as needed)
time_diff <= 3  # ±3 hours (adjust as needed)
```

### Change Memory Capacity:
```python
# In save_user_memory()
memory = memory[-100:]  # Keep last 100 (change number)
```

### Reset Learning:
Delete `user_override_memory.json` or:
```python
import os
if os.path.exists("user_override_memory.json"):
    os.remove("user_override_memory.json")
```

---

## 🌟 Future Enhancements

Potential improvements:
- **Weighted Learning**: Recent overrides matter more
- **Confidence Scores**: Show how certain AI is about recommendations
- **Explanation Depth**: More detailed reasoning chains
- **Pattern Visualization**: Charts showing learned preferences
- **Multi-Pattern Recognition**: Different routines for weekdays/weekends
- **Voice Commands**: "I'm always cold at night" → Adjusts evening preferences

---

## 📞 Troubleshooting

### AI Not Learning?
- Check if `user_override_memory.json` exists
- Verify manual overrides show "✅ AI learned from your action"
- Ensure LangGraph is available (no import errors)

### Recommendations Don't Match Memory?
- Need more overrides in similar conditions
- Check relevance filters (temperature/time thresholds)
- Review memory file to see what's actually stored

### Memory File Growing Too Large?
- Automatic cleanup keeps last 100 entries
- Manually delete old entries if needed
- System performance not affected until thousands of entries

---

## 📚 Key Files Modified

1. **`langgraph_agent.py`** - Core learning logic
2. **`live_simulation_dashboard.py`** - Manual override integration
3. **`user_override_memory.json`** - Persistent storage (auto-created)

---

## ✨ Summary

Your Smart Home AI now:
- 🧠 **Remembers** every manual adjustment you make
- 🎯 **Learns** your personal comfort preferences
- 🔮 **Predicts** what you would do in each situation
- 📈 **Evolves** to become more accurate over time
- 💡 **Explains** decisions based on your learned habits

**The more you use it, the smarter it gets!** 🚀
