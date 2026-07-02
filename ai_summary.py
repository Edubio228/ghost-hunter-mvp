# ai_summary.py
import os
from openai import OpenAI

# ==========================================
# READ TOKEN FROM ENVIRONMENT
# ==========================================
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize the OpenAI client pointed at OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    timeout=10.0,
)

def get_ai_roast(worst_ghost):
    prompt = f"""
    You are a strict, slightly sarcastic CFO. 
    Employee {worst_ghost['name']} hasn't committed code in {worst_ghost['github_gap_days']} days 
    and hasn't messaged on Slack in {worst_ghost['slack_gap_days']} days. 
    They cost the company ${worst_ghost['salary']} per month.
    
    Write one brutally funny, short corporate email to their manager recommending action. 
    Keep it to exactly 2 short sentences. Be professional but witty.
    """
    
    try:
        print("🤖 Asking OpenRouter to pick the best free model...")
        
        response = client.chat.completions.create(
            model="openrouter/auto",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            timeout=10.0,
            extra_headers={
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Ghost Hunter MVP",
            }
        )
        
        ai_message = response.choices[0].message.content
        print(f"✅ AI succeeded with OpenRouter auto-selection!")
        return ai_message
        
    except Exception as e:
        print(f"❌ AI failed: {str(e)[:100]}...")
        return f"⚠️ ALERT: {worst_ghost['name']} has been inactive for {worst_ghost['github_gap_days']} days. Recommend immediate license reclamation to save ${worst_ghost['salary']}/month."