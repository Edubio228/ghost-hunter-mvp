# app/auto_recover.py
import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# ==========================================
# READ CONFIGURATION FROM ENVIRONMENT
# ==========================================
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
GITHUB_ORG = os.getenv("GITHUB_ORG", "d33nAI")
SLACK_NOTIFICATION_CHANNEL = os.getenv("SLACK_NOTIFICATION_CHANNEL", "C09HGEUUXK8")
TEST_MODE = os.getenv("TEST_MODE", "True").lower() == "true"

# Initialize Slack client
slack_client = WebClient(token=SLACK_BOT_TOKEN)

def remove_user_from_github(username):
    """
    Removes a user from the GitHub organization.
    Returns: (success: bool, message: str)
    """
    if TEST_MODE:
        print(f"🧪 TEST MODE: Would remove @{username} from {GITHUB_ORG}")
        return True, f"🧪 TEST: Successfully removed @{username} (test mode)"
    
    if not GITHUB_TOKEN:
        return False, "❌ GitHub token not configured. Set GITHUB_TOKEN environment variable."
    
    if not GITHUB_ORG:
        return False, "❌ GitHub organization not configured. Set GITHUB_ORG environment variable."
    
    url = f"https://api.github.com/orgs/{GITHUB_ORG}/members/{username}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    try:
        response = requests.delete(url, headers=headers)
        
        if response.status_code == 204:
            return True, f"✅ Successfully removed @{username} from {GITHUB_ORG}"
        elif response.status_code == 404:
            return False, f"⚠️ User @{username} not found in {GITHUB_ORG}"
        elif response.status_code == 403:
            return False, f"⚠️ Permission denied. Token needs 'admin:org' scope."
        else:
            return False, f"❌ GitHub API error: {response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return False, f"❌ Network error: {str(e)}"

def send_slack_notification(ghost_name, github_username, salary, manager_email="the manager"):
    """
    Sends a Slack message to the notification channel about the recovery.
    """
    if TEST_MODE:
        print(f"🧪 TEST MODE: Would send Slack notification about {ghost_name}")
        return True, "🧪 TEST: Slack notification sent (test mode)"
    
    if not SLACK_BOT_TOKEN:
        return False, "❌ Slack token not configured. Set SLACK_BOT_TOKEN environment variable."
    
    if not SLACK_NOTIFICATION_CHANNEL:
        return False, "❌ Slack channel not configured. Set SLACK_NOTIFICATION_CHANNEL environment variable."
    
    try:
        message = f"""
🔔 *Ghost Recovery Alert*

*{ghost_name}* has been identified as a ghost employee:
• *GitHub Username:* @{github_username}
• *Monthly Salary:* ${salary:,}
• *Action Taken:* Removed from GitHub organization

Please follow up with HR to reclaim the license.
"""
        
        response = slack_client.chat_postMessage(
            channel=SLACK_NOTIFICATION_CHANNEL,
            text=message,
            mrkdwn=True
        )
        
        return True, "✅ Slack notification sent"
        
    except SlackApiError as e:
        return False, f"❌ Slack error: {e.response['error']}"
    except Exception as e:
        return False, f"❌ Unexpected error: {str(e)}"

def auto_recover_ghost(ghost_data):
    """
    Main function: removes ghost from GitHub and sends Slack notification.
    Returns: (success: bool, github_message: str, slack_message: str)
    """
    name = ghost_data['name']
    github_username = ghost_data['github_username']
    salary = ghost_data['salary']
    
    print(f"🔧 Attempting to recover {name} (@{github_username})...")
    
    github_success, github_msg = remove_user_from_github(github_username)
    slack_success, slack_msg = send_slack_notification(name, github_username, salary)
    
    overall_success = github_success and slack_success
    
    return overall_success, github_msg, slack_msg