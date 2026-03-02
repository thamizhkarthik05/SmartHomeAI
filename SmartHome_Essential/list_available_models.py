"""
List all available Gemini models for your API key
"""
import google.generativeai as genai

API_KEY = "AIzaSyAn1U4w3y1LcbGlOVEAq6Cg5Coc8acpLgA"

print("="*60)
print("🔍 Checking Available Gemini Models")
print("="*60)

try:
    genai.configure(api_key=API_KEY)
    
    print("\n📋 Available models:\n")
    
    models = genai.list_models()
    
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description[:80]}...")
            print()
    
    print("="*60)
    print("\n💡 Use one of these model names in your project")
    
except Exception as e:
    print(f"\n❌ Error listing models: {e}")
    print("\n💡 Your API key might not be valid or active")
