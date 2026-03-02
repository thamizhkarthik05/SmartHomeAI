# 🔮 Pattern Learning & Auto-Suggestion System

## Overview

The Smart Home AI now detects **confident patterns** from your manual overrides and can **auto-suggest** or **auto-apply** learned behaviors after reaching confidence thresholds.

---

## 🎯 How It Works

### **1. Data Collection** 📊

Every manual override stores:
```json
{
  "timestamp": "2025-11-06T10:12:39.318621",
  "temperature": 27.5,
  "humidity": 65,
  "occupancy": 1,
  "time_of_day": 14,
  "hvac_status": 0,
  "lighting": 75,
  "energy_usage": 1.5,
  "user_action": 1,
  "action_name": "❄️ Turn HVAC On"
}
```

### **2. Pattern Detection** 🔍

The system analyzes your overrides to find **repeating patterns**:

#### **Temperature-Based Patterns** (HVAC)
- Groups all instances where you took the same HVAC action
- Calculates average temperature and range
- Determines confidence based on frequency

**Example:**
```
Action: Turn HVAC On
Occurrences: 5 times
Temperature Range: 27.0°C - 28.2°C
Average: 27.6°C
Confidence: 100% (5 ÷ 3 threshold × 100)
```

#### **Time-Based Patterns** (Lighting)
- Groups all instances where you took the same lighting action
- Calculates average time and range
- Determines confidence based on frequency

**Example:**
```
Action: Decrease Lighting
Occurrences: 3 times
Time Range: 22:00 - 22:00
Average: 22:00
Confidence: 100% (3 ÷ 3 threshold × 100)
```

### **3. Confidence Levels** 📈

| Occurrences | Confidence | Emoji | Status |
|-------------|------------|-------|--------|
| 1-2 times   | < 66%      | 💫    | Learning |
| 3-4 times   | 66-99%     | ⭐    | Emerging |
| 5+ times    | 100%+      | 🔥    | **Confident** |

### **4. Auto-Suggestion** 💡

When a **confident pattern** matches current conditions:

```
Current State:
- Temperature: 27.4°C
- Time: 14:00

Detected Pattern:
- Action: Turn HVAC On
- Learned from: 5 times at ~27.6°C
- Confidence: 100%

Result: 🔮 Pattern Detected! Display suggestion
```

**Matching Criteria:**
- **Temperature patterns:** Within ±2°C of learned average
- **Time patterns:** Within ±1 hour of learned average

---

## 📱 Dashboard Features

### **Sidebar: Learned Patterns** 🎯

Located in: `🧠 AI Learning Status` → `🎯 Learned Patterns`

**Shows top 3 patterns:**
```
🔥 ❄️ Turn HVAC On
📍 27.6°C (range: 27.0-28.2°C)
✅ 5 times (100% confidence)
🤖 Auto-apply when temp ≈ 27.6°C

⭐ 🌙 Decrease Lighting
📍 22:00 (range: 22:00-22:00)
✅ 3 times (100% confidence)
🤖 Auto-apply around 22:00
```

### **Main Panel: Pattern Detection** 🔮

Located in: Right sidebar under "Current Status"

**When pattern matches:**
```
┌─────────────────────────────────┐
│ 🔮 Pattern Detected!            │
│                                 │
│ ❄️ Turn HVAC On                │
│                                 │
│ You've done this 5 times at     │
│ ~27.6°C                         │
│ Confidence: 100%                │
└─────────────────────────────────┘
```

---

## 🔧 Configuration

### **Confidence Threshold**

Default: **3 overrides** minimum for pattern detection

Change in code:
```python
# In langgraph_agent.py - detect_confident_patterns()
confidence_threshold = 3  # Minimum occurrences

# In dashboard - should_auto_apply()
should_auto_apply(current_state, confidence_threshold=5)  # For auto-suggestions
```

### **Matching Tolerance**

**Temperature matching:**
```python
if abs(current_temp - learned_avg_temp) <= 2:  # ±2°C tolerance
```

**Time matching:**
```python
if abs(current_time - learned_avg_time) <= 1:  # ±1 hour tolerance
```

---

## 📊 Pattern Analysis Examples

### **Example 1: Morning Lighting Routine**

**User Actions:**
```
Day 1: 07:00 - Increase Lighting (from 20% to 60%)
Day 2: 07:15 - Increase Lighting (from 30% to 70%)
Day 3: 06:45 - Increase Lighting (from 25% to 65%)
Day 4: 07:00 - Increase Lighting (from 20% to 60%)
Day 5: 07:10 - Increase Lighting (from 35% to 75%)
```

**Detected Pattern:**
- Action: 💡 Increase Lighting
- Time Range: 06:45 - 07:15
- Average Time: 07:00
- Occurrences: 5
- Confidence: 166% (5 ÷ 3 × 100)
- Status: 🔥 Highly Confident

**Auto-Suggestion Trigger:**
- When time is between 06:00 - 08:00
- And lighting < 60%
- System suggests: "Increase Lighting"

### **Example 2: Temperature Comfort Zone**

**User Actions:**
```
Week 1: 27.2°C - Turn HVAC On
Week 1: 27.8°C - Turn HVAC On
Week 2: 26.9°C - Turn HVAC On
Week 2: 28.1°C - Turn HVAC On
Week 3: 27.5°C - Turn HVAC On
```

**Detected Pattern:**
- Action: ❄️ Turn HVAC On
- Temp Range: 26.9°C - 28.1°C
- Average Temp: 27.5°C
- Occurrences: 5
- Confidence: 166%
- Status: 🔥 Highly Confident

**Auto-Suggestion Trigger:**
- When temp is between 25.5°C - 29.5°C (±2°C)
- And HVAC is currently OFF
- System suggests: "Turn HVAC On"

### **Example 3: Evening Wind-Down**

**User Actions:**
```
Night 1: 22:00 - Decrease Lighting
Night 2: 22:00 - Decrease Lighting  
Night 3: 21:45 - Decrease Lighting
Night 4: 22:15 - Decrease Lighting
```

**Detected Pattern:**
- Action: 🌙 Decrease Lighting
- Time Range: 21:45 - 22:15
- Average Time: 22:00
- Occurrences: 4
- Confidence: 133%
- Status: 🔥 Confident

**Auto-Suggestion Trigger:**
- When time is between 21:00 - 23:00
- And lighting > 50%
- System suggests: "Decrease Lighting"

---

## 🚀 Evolution Over Time

### **Phase 1: Initial Learning** (1-2 overrides)
- 💫 System observes your actions
- No patterns detected yet
- Gemini AI uses general recommendations

### **Phase 2: Pattern Emergence** (3-4 overrides)
- ⭐ Patterns starting to form
- Shows in "Learned Patterns" section
- Gemini AI mentions "you've adjusted before"

### **Phase 3: Confident Patterns** (5+ overrides)
- 🔥 Strong patterns established
- Auto-suggestions appear in UI
- Gemini AI prioritizes your learned preferences
- System can predict your actions

### **Phase 4: Habit Automation** (10+ overrides)
- 🎯 Very high confidence
- Multiple patterns for different scenarios
- Proactive suggestions
- Minimal manual intervention needed

---

## 💡 Use Cases

### **1. Energy-Conscious User**
```
Pattern: Turn HVAC Off when temp drops to 23°C
Learning: After 5 times, system suggests it automatically
Benefit: Saves energy without thinking about it
```

### **2. Night Owl**
```
Pattern: Dim lights at 23:00 every night
Learning: After 3 nights, system recognizes routine
Benefit: Automatic evening ambiance
```

### **3. Temperature Sensitive**
```
Pattern: HVAC On at 26°C (lower than default 27°C)
Learning: After 6 overrides, system learns preference
Benefit: Proactive cooling at YOUR comfort level
```

### **4. Work-from-Home Schedule**
```
Pattern 1: Bright lights (80%) at 09:00 (work start)
Pattern 2: Dim lights (40%) at 17:00 (work end)
Learning: After a week, system knows your schedule
Benefit: Automatic workspace optimization
```

---

## 🔬 Technical Details

### **Pattern Detection Algorithm**

```python
def detect_confident_patterns(memory, confidence_threshold=3):
    """
    1. Group overrides by action type (HVAC vs Lighting)
    2. For each action group:
       - Calculate average trigger value (temp or time)
       - Calculate range of occurrences
       - Compute confidence: (occurrences / threshold) × 100
    3. Filter patterns with confidence >= threshold
    4. Sort by confidence (highest first)
    5. Return top patterns
    """
```

### **Auto-Apply Decision Logic**

```python
def should_auto_apply(current_state, confidence_threshold=5):
    """
    1. Load all patterns with confidence >= 100%
    2. For each high-confidence pattern:
       - Check if current state matches trigger conditions
       - Temperature: ±2°C tolerance
       - Time: ±1 hour tolerance
    3. Return first matching pattern as suggestion
    4. If no match, return {"should_apply": False}
    """
```

### **Data Storage**

All patterns derived from: `user_override_memory.json`

**Memory limit:** 100 most recent overrides (prevents file bloat)

**Persistence:** Survives app restarts

**Privacy:** Local storage only, no cloud

---

## 📈 Benefits

### **For Users:**
1. ✅ **Less Manual Work** - System learns and suggests
2. ✅ **Personalized Comfort** - Based on YOUR actions
3. ✅ **Transparent Learning** - See what AI learned
4. ✅ **Confidence Levels** - Know how sure the system is
5. ✅ **Override Anytime** - You're always in control

### **For the AI:**
1. ✅ **Better Predictions** - Learns from real behavior
2. ✅ **Contextual Awareness** - Knows when patterns apply
3. ✅ **Continuous Improvement** - Gets smarter over time
4. ✅ **Explainable** - Can show why it suggests actions

---

## 🎓 Best Practices

### **To Build Strong Patterns:**

1. **Be Consistent** 
   - Do the same action in similar situations
   - Example: Always turn HVAC on around 27°C

2. **Give It Time**
   - 5+ overrides for confident patterns
   - 3+ for emerging patterns

3. **Create Routines**
   - Same actions at same times
   - Example: Dim lights every night at 10 PM

4. **Review Patterns**
   - Check sidebar "Learned Patterns"
   - Adjust if system learned incorrectly

### **To Override Learned Patterns:**

- Just use manual controls differently
- New data will update patterns
- Old patterns fade if not repeated

---

## 🔮 Future Enhancements

Potential additions:

1. **One-Click Auto-Apply**
   - Button to instantly apply suggestion
   
2. **Pattern Scheduling**
   - "Apply this pattern daily at X time"
   
3. **Multi-Factor Patterns**
   - Combine temp + time + occupancy
   
4. **Pattern Export/Import**
   - Share learned routines
   
5. **Weekly Pattern Analysis**
   - Dashboard showing pattern evolution

---

## 📊 Monitoring Your Patterns

### **Dashboard Indicators:**

**Sidebar Stats:**
- Total overrides count
- Most common action
- Top 3 learned patterns with confidence

**Pattern Detection Box:**
- Appears when confident pattern matches
- Shows reason and confidence level
- Real-time suggestion

**Gemini AI Reasoning:**
- References your past overrides
- Mentions pattern confidence
- Explains how it learned

---

## ✅ Summary

**The Pattern Learning System:**

1. 📝 **Records** every manual override with context
2. 🔍 **Analyzes** to find repeating behaviors  
3. 📊 **Calculates** confidence based on frequency
4. 💡 **Suggests** actions when patterns match
5. 🔮 **Predicts** what you'll likely do next
6. 🎯 **Evolves** as you use the system more

**After 5+ similar overrides:**
- System knows your preference
- Auto-suggests in matching situations
- Gemini AI prioritizes your learned pattern
- You see confidence levels in dashboard

**You're teaching the AI to think like YOU!** 🧠✨
