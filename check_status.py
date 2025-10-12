import os
import sys

print("="*60)
print("🔍 SMART HOME AI PROJECT STATUS CHECK")
print("="*60)

# Check for required files
files_to_check = {
    "📊 Dataset (NEW)": "SmartHome_Realistic_Dataset.csv",
    "📊 Dataset (OLD)": "SmartHome_Environment_v1.csv",
    "🧠 Trained Model": "smart_home_ai_brain.zip",
    "🏠 Environment": "environment.py",
    "🎓 Training Script": "train.py",
    "🧪 Test Script": "test_agent.py",
    "📈 Dashboard": "enhanced_dashboard.py",
    "🔧 Generator": "generate_realistic_dataset.py",
}

print("\n📁 FILE STATUS:")
print("-"*60)

all_good = True
missing_critical = []

for name, filename in files_to_check.items():
    exists = os.path.exists(filename)
    status = "✅" if exists else "❌"
    print(f"{status} {name}: {filename}")
    
    if not exists:
        if "NEW" in name or "Model" in name or "Environment" in name:
            all_good = False
            missing_critical.append((name, filename))

# Check if packages are installed
print("\n📦 PACKAGE STATUS:")
print("-"*60)

packages_to_check = [
    "gymnasium",
    "stable_baselines3", 
    "pandas",
    "numpy",
    "matplotlib",
    "streamlit",
    "plotly"
]

missing_packages = []

for package in packages_to_check:
    try:
        __import__(package)
        print(f"✅ {package}")
    except ImportError:
        print(f"❌ {package} - NOT INSTALLED")
        missing_packages.append(package)
        all_good = False

# Recommendations
print("\n" + "="*60)
print("💡 RECOMMENDATIONS")
print("="*60)

if missing_packages:
    print("\n❌ Missing packages detected!")
    print("   Run: pip install -r requirements.txt")
    print()

if missing_critical:
    print("\n⚠️ Missing critical files:")
    for name, filename in missing_critical:
        if "NEW" in name:
            print(f"\n   {name}: {filename}")
            print(f"   → Run: python generate_realistic_dataset.py")
        elif "Model" in name:
            print(f"\n   {name}: {filename}")
            print(f"   → Run: python train.py")

if all_good:
    print("\n🎉 ✅ ALL SYSTEMS GO!")
    print("\n🚀 You can now:")
    print("   1. Train the model: python train.py")
    print("   2. Test the model: python test_agent.py")
    print("   3. Run dashboard: streamlit run enhanced_dashboard.py")
else:
    print("\n⚠️ Some issues detected. Follow the recommendations above.")

print("\n" + "="*60)

# Additional guidance
if not os.path.exists("SmartHome_Realistic_Dataset.csv"):
    print("\n🔴 CRITICAL: NEW dataset not found!")
    print("   This dataset is REQUIRED for proper training.")
    print("   The old dataset (SmartHome_Environment_v1.csv) is NOT suitable.")
    print("\n   ▶️ NEXT STEP: python generate_realistic_dataset.py")
    print("="*60)
    sys.exit(1)

if not os.path.exists("smart_home_ai_brain.zip"):
    print("\n⚠️ WARNING: Trained model not found!")
    print("   You need to train the model before testing.")
    print("\n   ▶️ NEXT STEP: python train.py")
    print("="*60)
    sys.exit(1)

if all_good and os.path.exists("SmartHome_Realistic_Dataset.csv") and os.path.exists("smart_home_ai_brain.zip"):
    print("\n✨ READY FOR TESTING!")
    print("   ▶️ NEXT STEP: python test_agent.py")
    print("   Or run dashboard: streamlit run enhanced_dashboard.py")
    print("="*60)
