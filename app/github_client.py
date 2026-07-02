# app/github_client.py
import os
import requests
from datetime import datetime, date

# ==========================================
# READ TOKEN FROM ENVIRONMENT
# ==========================================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_last_commit_date(github_username):
    """
    Asks GitHub: "When did this user last push code to any public repository?"
    Returns a Python 'date' object, or None if we can't find any commits.
    """
    
    if not github_username or github_username == "unknown":
        return None
        
    url = f"https://api.github.com/users/{github_username}/events/public"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 404:
            print(f"⚠️ User '{github_username}' not found on GitHub.")
            return None
            
        if response.status_code == 401:
            print("❌ Invalid GitHub token! Please check your GITHUB_TOKEN environment variable.")
            return None
            
        if response.status_code == 403:
            print(f"⚠️ Rate limit hit for {github_username}.")
            return None
            
        response.raise_for_status()
        events = response.json()
        
        for event in events:
            if event['type'] == 'PushEvent':
                last_commit_str = event['created_at']
                last_commit_date = datetime.fromisoformat(last_commit_str.replace('Z', '+00:00')).date()
                return last_commit_date
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error for {github_username}: {e}")
        return None