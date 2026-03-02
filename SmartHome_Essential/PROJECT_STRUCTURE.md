# Smart Home AI - Essential Files

This folder contains ONLY the essential files needed to run the Smart Home AI project.

## 📁 Core Files

### Training & Environment
- **`train.py`** - Train the DQN model
- **`environment.py`** - Training environment (uses dataset)
- **`interactive_environment.py`** - Live simulation environment (synthetic)
- **`SmartHome_Realistic_Dataset.csv`** - Training dataset

### AI Agent & Dashboard
- **`langgraph_agent.py`** - Gemini AI agent with pattern learning
- **`live_simulation_dashboard.py`** - Main Streamlit dashboard
- **`user_override_memory.json`** - Stores manual override history (max 100 entries)

### Trained Model
- **`smart_home_ai_brain.zip`** - Trained DQN model (ready to use)

### Testing & Validation
- **`test_agent.py`** - Quick test run
- **`verify_model.py`** - Comprehensive verification
- **`validate_training.py`** - Training quality analysis

### Dependencies & Documentation
- **`requirements.txt`** - Python package dependencies
- **`README.md`** - Project overview
- **`AI_LEARNING_SYSTEM.md`** - Learning system documentation
- **`PATTERN_LEARNING.md`** - Pattern detection guide
- **`LIVE_SIMULATION_GUIDE.md`** - Dashboard usage guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Your Gemini API Key
Edit line 13 in `langgraph_agent.py`:
```python
API_KEY = "your-api-key-here"
```

### 3. Run the Dashboard
```bash
streamlit run live_simulation_dashboard.py
```

### 4. Test the Model
```bash
python verify_model.py
```

## 📊 What Each Component Does

| Component | Purpose |
|-----------|---------|
| **DQN Model** | Makes smart home control decisions |
| **Gemini AI** | Provides explanations & learns from overrides |
| **Pattern Detection** | Learns user preferences over time |
| **Dashboard** | Real-time visualization & manual control |

## 🎯 Typical Workflow

1. **Train** (if needed): `python train.py`
2. **Verify**: `python verify_model.py`
3. **Run Dashboard**: `streamlit run live_simulation_dashboard.py`
4. **Use manual overrides** → System learns your patterns
5. **Get auto-suggestions** when patterns are confident

## 🔧 Configuration

- **Memory Limit**: 100 overrides (change in `langgraph_agent.py` line 45)
- **Pattern Threshold**: 3 for detection, 5 for auto-apply (line 138)
- **Temperature Tolerance**: ±2°C (line 152)
- **Time Tolerance**: ±1 hour (line 153)

---

All other files in the parent directory are legacy/experimental versions not needed for current functionality.
