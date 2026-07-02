# app/slack_client.py
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import date, timedelta
import time
from typing import Dict, Optional

# ==========================================
# READ TOKEN FROM ENVIRONMENT
# ==========================================
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# Initialize the Slack client
client = WebClient(token=SLACK_BOT_TOKEN)

def get_all_users() -> Dict[str, str]:
    """
    Fetches a list of all users in the workspace.
    Returns a dictionary: { 'user_id': 'display_name', ... }
    """
    try:
        response = client.users_list()
        users = {}
        members = response.get('members', [])
        if members is None:
            members = []
            
        for user in members:
            if not user.get('is_bot', False) and not user.get('deleted', False):
                if user['id'] == "USLACKBOT":
                    continue
                name = user.get('real_name') or user.get('name') or "Unknown"
                users[user['id']] = name
        return users
        
    except SlackApiError as e:
        print(f"🚨 Slack API Error (users.list): {e.response['error']}")
        return {}

def get_last_active_date(user_id: str) -> Optional[date]:
    """
    Gets the user's last activity date using users.getPresence.
    This does NOT require im:history scope!
    """
    try:
        response = client.users_getPresence(user=user_id)
        
        if response.get('presence') == 'active':
            return date.today()
        
        last_activity = response.get('last_activity')
        if last_activity:
            last_activity_date = date.fromtimestamp(last_activity)
            return last_activity_date
        
        return None
        
    except SlackApiError as e:
        if e.response['error'] not in ['user_not_found', 'invalid_user']:
            print(f"🚨 Slack API Error for user {user_id}: {e.response['error']}")
        return None
    except Exception as e:
        print(f"🚨 Unexpected error for user {user_id}: {e}")
        return None

def get_last_message_date_for_all_users() -> Dict[str, date]:
    """
    Fetches last active date for EVERY user in the workspace.
    Returns: { 'user_id': date_object, ... }
    """
    print("📡 Fetching user list from Slack...")
    all_users = get_all_users()
    
    if not all_users:
        print("⚠️ No users found. Check your token and permissions.")
        return {}
    
    print(f"✅ Found {len(all_users)} users. Fetching last activity dates...")
    
    user_last_active = {}
    total_users = len(all_users)
    
    for i, (user_id, user_name) in enumerate(all_users.items(), 1):
        print(f"  🔍 Checking Slack for: {user_name} ({i}/{total_users})...")
        last_date = get_last_active_date(user_id)
        if last_date:
            user_last_active[user_id] = last_date
        time.sleep(0.1)
    
    print(f"✅ Found last activity dates for {len(user_last_active)} users.")
    return user_last_active