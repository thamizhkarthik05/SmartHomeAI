"""
Verify which API key is being used across all project files
"""

import re

# Files that use API key
files_to_check = {
    "langgraph_agent.py": "Project main file",
    "test_api_key.py": "API test script"
}

print("="*60)
print("🔍 API KEY VERIFICATION REPORT")
print("="*60)

api_keys = {}

for filename, description in files_to_check.items():
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find API_KEY = "..." pattern
            match = re.search(r'API_KEY\s*=\s*["\']([^"\']+)["\']', content)
            if match:
                api_key = match.group(1)
                api_keys[filename] = api_key
                print(f"\n📄 {filename}")
                print(f"   ({description})")
                print(f"   🔑 Key: {api_key[:20]}...{api_key[-4:]}")
            else:
                print(f"\n📄 {filename}")
                print(f"   ❌ No API key found!")
    except FileNotFoundError:
        print(f"\n📄 {filename}")
        print(f"   ⚠️  File not found")

# Check if all keys match
print("\n" + "="*60)
unique_keys = set(api_keys.values())

if len(unique_keys) == 1:
    print("✅ ALL FILES USE THE SAME API KEY!")
    print(f"   Key: {list(unique_keys)[0][:20]}...{list(unique_keys)[0][-4:]}")
elif len(unique_keys) > 1:
    print("⚠️  WARNING: DIFFERENT API KEYS FOUND!")
    for filename, key in api_keys.items():
        print(f"   {filename}: ...{key[-8:]}")
    print("\n   ⚠️  Files should use the same key!")
else:
    print("❌ No API keys found in any files")

print("="*60)

# Show current key being used
if "langgraph_agent.py" in api_keys:
    print(f"\n🎯 PROJECT IS USING: {api_keys['langgraph_agent.py']}")
    print("   (This is the key used by the dashboard)")
print()
