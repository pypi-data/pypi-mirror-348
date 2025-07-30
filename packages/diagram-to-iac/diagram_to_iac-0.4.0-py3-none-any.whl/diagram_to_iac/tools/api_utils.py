import sys
import os
from openai import OpenAI
from anthropic import Anthropic
import requests
import google.generativeai as genai
import googleapiclient.discovery
# Add the parent directory to sys.path to import env_loader
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from scripts.env_loader import load_env_keys

def test_openai_api():
    try:
        if not os.environ.get("OPENAI_API_KEY"):
            print("❌ OpenAI API error: OPENAI_API_KEY environment variable not set.")
            return False
        client = OpenAI()
        response = client.chat.completions.create(
            # Consider using a newer model if appropriate, e.g., "gpt-4o-mini" or "gpt-3.5-turbo"
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=10
        )
        return True
    except Exception as e:
        print(f"❌ Open AI API error: {str(e)}")
        return False

def test_gemini_api():
    try:
        google_api_key = os.environ.get("GOOGLE_API_KEY")
        if not google_api_key:
            print("❌ Gemini API error: GOOGLE_API_KEY environment variable not set.")
            return False
        genai.configure(api_key=google_api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Corrected model name
        response = model.generate_content("Hello, are you working?")
        return True
    except Exception as e:
        print(f"❌ Gemini API error: {str(e)}")
        return False

def test_anthropic_api():
    try:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            print("❌ Anthropic API error: ANTHROPIC_API_KEY environment variable not set.")
            return False
        client = Anthropic()
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hello, are you working?"}]
        )
        return True
    except Exception as e:
        print(f"❌ Anthropic API error: {str(e)}")
        return False

def test_github_api():
    """Test the GitHub API connection."""
    try:      
        token = os.environ.get("GITHUB_TOKEN")
        if not token: # This check is already good
            print("❌ GitHub API error: GITHUB_TOKEN environment variable not set")
            return False
            
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Try to get the authenticated user
        url = "https://api.github.com/user"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            username = user_data.get('login')
            print(f"✅ GitHub API works! Authenticated as: {username}")
            return True
        else:
            print(f"❌ GitHub API error: Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ GitHub API error: {str(e)}")
        return False

def test_all_apis():
    print("Hello from the test workflow!")
    print("Loading environment keys...")
    # Load environment keys once before running all tests
    #load_env_keys()
    
    print("Testing API connections...")
    openai_success = test_openai_api()
    gemini_success = test_gemini_api()
    anthropic_success = test_anthropic_api()
    github_success = test_github_api()  # Added GitHub API test
    
    print("\nSummary:")
    print(f"OpenAI API: {'✅ Working' if openai_success else '❌ Failed'}")
    print(f"Gemini API: {'✅ Working' if gemini_success else '❌ Failed'}")
    print(f"Anthropic API: {'✅ Working' if anthropic_success else '❌ Failed'}")
    print(f"GitHub API: {'✅ Working' if github_success else '❌ Failed'}")  # Added GitHub API result
    
    if openai_success and gemini_success and anthropic_success and github_success:  # Updated condition
        print("\n🎉 All APIs are working correctly!")
    else:
        print("\n⚠️ Some APIs failed. Check the errors above.")
