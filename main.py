import os
from dotenv import load_dotenv

# Load environment variables from .env file (only for local development)
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import ghost_hunter
import ai_summary
import auto_recover

app = FastAPI()
@app.get("/", response_class=HTMLResponse)
async def show_dashboard():
    # 1. Get the ghost list from our hunter
    ghost_list = ghost_hunter.find_ghosts("employees.csv")
    
    # 2. Find the absolute worst ghost (for the AI roast)
    top_ghost = ghost_list[0]
    
    # 3. Get the AI roast message
    ai_message = ai_summary.get_ai_roast(top_ghost)
    
    # ============================================================
    # CALCULATE TOTAL MONTHLY SAVINGS
    # ============================================================
    # Ghosts are defined as people with a score >= 60
    ghosts = [person for person in ghost_list if person['score'] >= 60]
    total_savings = sum(person['salary'] for person in ghosts)
    ghost_count = len(ghosts)
    
    # Format the number with commas (e.g., 29,400)
    total_savings_formatted = f"{total_savings:,}"
    
    # ============================================================
    # BUILD THE HTML PAGE
    # ============================================================
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ghost Hunter MVP</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Arial, sans-serif; 
                background: #f4f4f9; 
                padding: 40px; 
                margin: 0;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            h1 {{ color: #2c3e50; font-weight: 300; border-bottom: 2px solid #eee; padding-bottom: 15px; }}
            
            /* ---- AI Alert Box ---- */
            .alert {{ 
                background: #fff3cd; 
                border-left: 5px solid #ffc107; 
                padding: 15px 20px; 
                margin-bottom: 25px; 
                border-radius: 5px; 
                color: #856404;
                font-size: 1.1em;
            }}
            
            /* ---- SAVINGS CARD ---- */
            .savings-card {{
                background: linear-gradient(135deg, #11998e, #38ef7d);
                border-radius: 12px;
                padding: 25px 30px;
                margin-bottom: 30px;
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4);
            }}
            .savings-card .left {{
                display: flex;
                flex-direction: column;
            }}
            .savings-card .label {{
                font-size: 1.0em;
                opacity: 0.9;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 300;
            }}
            .savings-card .amount {{
                font-size: 3.2em;
                font-weight: 700;
                line-height: 1.2;
            }}
            .savings-card .subtitle {{
                font-size: 0.95em;
                opacity: 0.85;
                margin-top: 5px;
            }}
            .savings-card .right {{
                background: rgba(255,255,255,0.2);
                padding: 10px 20px;
                border-radius: 50px;
                font-size: 1.4em;
                font-weight: 600;
                text-align: center;
            }}
            .savings-card .right small {{
                display: block;
                font-size: 0.5em;
                font-weight: 300;
                opacity: 0.8;
            }}
            
            /* ---- Table ---- */
            table {{ 
                width: 100%; 
                border-collapse: collapse; 
                background: white; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.08); 
                border-radius: 8px;
                overflow: hidden;
            }}
            th {{ 
                background: #2c3e50; 
                color: white; 
                padding: 14px 16px; 
                text-align: left; 
                font-weight: 500;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            td {{ 
                padding: 12px 16px; 
                border-bottom: 1px solid #eee; 
            }}
            tr:last-child td {{ border-bottom: none; }}
            tr:hover td {{ background: #f8f9fa; }}
            
            /* ---- Badges ---- */
            .badge {{ 
                padding: 5px 12px; 
                border-radius: 20px; 
                font-weight: 600; 
                font-size: 0.8em;
                white-space: nowrap;
            }}
            .badge-ghost {{ background: #f44336; color: white; }}
            .badge-sus {{ background: #ff9800; color: white; }}
            .badge-active {{ background: #4caf50; color: white; }}
            
            /* ---- Auto-Recover Button ---- */
            .recover-btn {{
                background: #dc3545;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.8em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                margin-left: 8px;
            }}
            .recover-btn:hover {{
                background: #c82333;
                transform: scale(1.05);
            }}
            .recover-btn:disabled {{
                background: #6c757d;
                cursor: not-allowed;
                transform: none;
            }}
            .recover-btn.loading {{
                background: #ffc107;
                color: #333;
            }}
            .recover-btn.success {{
                background: #28a745;
            }}
            .recover-btn.error {{
                background: #dc3545;
            }}
            
            .footer {{
                margin-top: 20px;
                color: #777;
                font-size: 0.9em;
                text-align: center;
                border-top: 1px solid #ddd;
                padding-top: 20px;
            }}
    </style>
    </head>
    <body>
        <div class="container">
            <h1>👻 HR Ghost Hunter Dashboard</h1>
            
            <!-- AI Alert -->
            <div class="alert">
                <strong>🤖 AI Agent says:</strong> {ai_message}
            </div>
            
            <!-- SAVINGS CARD -->
            <div class="savings-card">
                <div class="left">
                    <span class="label">💰 Total Monthly Savings Opportunity</span>
                    <span class="amount">${total_savings_formatted}</span>
                    <span class="subtitle">By reclaiming licenses from {ghost_count} ghost employee(s)</span>
                </div>
                <div class="right">
                    {ghost_count}
                    <small>Ghosts Found</small>
                </div>
            </div>

            <h2>Employee Audit Report (Sorted by Ghost Score)</h2>
            
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Team</th>
                        <th>Salary (Monthly)</th>
                        <th>Days since Code</th>
                        <th>Days since Slack</th>
                        <th>Ghost Score</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Loop through the results to build the table rows
    for person in ghost_list:
        # Pick a color for the status badge
        if person['status'] == "GHOST - Reclaim License!":
            badge_class = "badge-ghost"
            show_recover_button = True  # Show button for ghosts
        elif person['status'] == "Suspicious - Check manually":
            badge_class = "badge-sus"
            show_recover_button = False
        else:
            badge_class = "badge-active"
            show_recover_button = False
        
        # Escape the name for use in JavaScript (in case it has quotes)
        escaped_name = person['name'].replace("'", "\\'").replace('"', '&quot;')
            
        # Add a new row to the table
        html_content += f"""
            <tr>
                <td><strong>{person['name']}</strong></td>
                <td>{person['team']}</td>
                <td>${person['salary']:,}</td>
                <td>{person['github_gap_days']} days</td>
                <td>{person['slack_gap_days']} days</td>
                <td>{person['score']} / 100</td>
                <td>
                    <span class="badge {badge_class}">{person['status']}</span>
        """
        
        # Add the Auto-Recover button ONLY if it's a ghost
        if show_recover_button:
            html_content += f"""
                    <button 
                        class="recover-btn" 
                        onclick="recoverGhost('{escaped_name}')"
                        data-name="{person['name']}"
                    >
                        ⚡ Recover
                    </button>
            """
        
        html_content += f"""
                </td>
            </tr>
        """
    
    # Close the HTML tags
    html_content += f"""
                </tbody>
            </table>
            <div class="footer">
                * Built with real data from GitHub & Slack APIs. 
                Total potential savings: <strong>${total_savings_formatted}/month</strong>.
            </div>
        </div>
        
        <!-- ========================================================== -->
        <!-- JAVASCRIPT FOR AUTO-RECOVER                                 -->
        <!-- ========================================================== -->
        <script>
            function recoverGhost(name) {{
                // Find the button for this specific ghost
                const button = document.querySelector(`.recover-btn[data-name="${{name}}"]`);
                if (!button) return;
                
                // Disable the button and show loading state
                button.disabled = true;
                button.textContent = '⏳ Processing...';
                button.className = 'recover-btn loading';
                
                // Send the recovery request
                fetch(`/recover/${{encodeURIComponent(name)}}`, {{
                    method: 'POST',
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        button.textContent = '✅ Recovered!';
                        button.className = 'recover-btn success';
                        // Refresh the page after 2 seconds to update the dashboard
                        setTimeout(() => {{
                            location.reload();
                        }}, 2000);
                    }} else {{
                        button.textContent = '❌ Failed';
                        button.className = 'recover-btn error';
                        // Show the error message in an alert
                        alert(`Recovery failed: ${{data.message}}`);
                        // Re-enable after 3 seconds so they can try again
                        setTimeout(() => {{
                            button.disabled = false;
                            button.textContent = '⚡ Recover';
                            button.className = 'recover-btn';
                        }}, 3000);
                    }}
                }})
                .catch(error => {{
                    button.textContent = '❌ Error';
                    button.className = 'recover-btn error';
                    alert(`Network error: ${{error.message}}`);
                    setTimeout(() => {{
                        button.disabled = false;
                        button.textContent = '⚡ Recover';
                        button.className = 'recover-btn';
                    }}, 3000);
                }});
            }}
        </script>
        
    </body>
    </html>
    """
    
    return html_content

# ============================================================
# AUTO-RECOVER API ENDPOINT
# ============================================================
@app.post("/recover/{name}")
async def recover_ghost(name: str):
    """
    API endpoint that recovers a ghost by removing them from GitHub
    and sending a Slack notification.
    """
    # 1. Get the latest ghost list
    ghost_list = ghost_hunter.find_ghosts("employees.csv")
    
    # 2. Find the ghost with the matching name
    target_ghost = None
    for person in ghost_list:
        if person['name'].lower() == name.lower():
            target_ghost = person
            break
    
    if not target_ghost:
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": f"Ghost '{name}' not found"}
        )
    
    # 3. Check if they're actually a ghost (score >= 60)
    if target_ghost['score'] < 60:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": f"{name} is not a ghost (score: {target_ghost['score']})"}
        )
    
    # 4. Perform the recovery
    success, github_msg, slack_msg = auto_recover.auto_recover_ghost(target_ghost)
    
    return {
        "success": success,
        "message": f"Recovery for {name}: {github_msg} | {slack_msg}",
        "github": github_msg,
        "slack": slack_msg
    }