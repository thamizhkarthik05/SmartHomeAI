"""
Script to fix model compatibility by re-saving with current environment
"""
import sys
import os

# NumPy compatibility fix
import numpy as np
if not hasattr(np, '_core'):
    import numpy.core as _core
    np._core = _core

from stable_baselines3 import DQN
from environment import SmartHomeEnv

print("🔧 Fixing model compatibility...")
print(f"NumPy version: {np.__version__}")

try:
    # Try to load the model
    print("\n📂 Loading model...")
    model = DQN.load("smart_home_ai_brain.zip", print_system_info=False)
    
    print("✅ Model loaded successfully!")
    
    # Re-save with current environment
    print("\n💾 Re-saving model with current environment...")
    model.save("smart_home_ai_brain_fixed")
    
    print("✅ Model re-saved as 'smart_home_ai_brain_fixed.zip'")
    
    # Backup old and rename new
    if os.path.exists("smart_home_ai_brain.zip"):
        os.rename("smart_home_ai_brain.zip", "smart_home_ai_brain_backup.zip")
        print("📦 Old model backed up as 'smart_home_ai_brain_backup.zip'")
    
    os.rename("smart_home_ai_brain_fixed.zip", "smart_home_ai_brain.zip")
    print("✅ Fixed model renamed to 'smart_home_ai_brain.zip'")
    
    print("\n🎉 Model compatibility fixed! You can now run the dashboard.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nError type: {type(e).__name__}")
    print("\n💡 This might be a serious compatibility issue.")
    print("You may need to retrain the model with: python train.py")
    sys.exit(1)
