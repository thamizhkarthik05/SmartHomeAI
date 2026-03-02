"""
Quick test to verify Gemini API key is working
"""
import google.generativeai as genai

# Your API key (MUST match the one in langgraph_agent.py)
API_KEY = "AIzaSyAn1U4w3y1LcbGlOVEAq6Cg5Coc8acpLgA"

print("Testing Gemini API Key...")
print("="*50)
print(f"🔑 Testing API Key: {API_KEY[:20]}...{API_KEY[-4:]}")
print("="*50)

try:
    # Configure the API
    genai.configure(api_key=API_KEY)
    
    # Initialize model (using gemini-2.5-flash - stable with large context)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Send a simple test prompt
    print("\n📡 Sending test request to Gemini...")
    response = model.generate_content("Say 'Hello! API is working!' in one sentence.")
    
    # Display result
    print("\n✅ SUCCESS! API Key is working!")
    print(f"\n🤖 Gemini Response:\n{response.text}")
    print("\n" + "="*50)
    print("✅ Your API key is valid and functional!")
    
except Exception as e:
    print(f"\n❌ ERROR: API Key test failed!")
    print(f"\n🔴 Error details: {e}")
    print("\n💡 Possible issues:")
    print("   - API key is invalid or expired")
    print("   - API key doesn't have proper permissions")
    print("   - Network connection issue")
    print("   - Gemini API service is down")
    print("\n" + "="*50)
