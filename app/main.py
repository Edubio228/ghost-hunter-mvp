# app/main.py
import os
import io
import csv
from datetime import timedelta
from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import get_db, init_db
from .models import User, Company, CompanySettings
from .auth import (
    authenticate_user, create_access_token,
    get_current_user_from_cookie,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from . import ghost_hunter, ai_summary, auto_recover

app = FastAPI(title="Ghost Hunter", version="1.0.0")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Initialize database
init_db()

@app.on_event("startup")
async def startup():
    """Create default admin user on first startup"""
    db = next(get_db())
    
    if db.query(User).count() == 0:
        company = Company(
            name="Demo Company",
            github_org="d33nAI",
            slack_channel="C09HGEUUXK8"
        )
        db.add(company)
        db.flush()
        
        hashed = get_password_hash("admin123")
        admin = User(
            email="admin@demo.com",
            password_hash=hashed,
            full_name="Admin User",
            company_id=company.id,
            role="admin"
        )
        db.add(admin)
        
        settings = CompanySettings(
            company_id=company.id,
            test_mode=True,
            auto_recover_enabled=False
        )
        db.add(settings)
        
        db.commit()
        print("✅ Default admin created: admin@demo.com / admin123")
        print("✅ Demo company created: d33nAI")

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    """Main dashboard showing ghost list"""
    ghost_list = ghost_hunter.find_ghosts("employees.csv")
    
    ghosts = [p for p in ghost_list if p['score'] >= 60]
    active = [p for p in ghost_list if p['score'] < 20]
    suspicious = [p for p in ghost_list if 20 <= p['score'] < 60]
    
    total_savings = sum(p['salary'] for p in ghosts)
    total_savings_formatted = f"{total_savings:,}"
    
    top_ghost = ghost_list[0]
    ai_message = ai_summary.get_ai_roast(top_ghost)
    
    return templates.TemplateResponse(request, "dashboard.html", {
        "ghost_list": ghost_list,
        "ghost_count": len(ghosts),
        "active_count": len(active),
        "suspicious_count": len(suspicious),
        "total_savings_formatted": total_savings_formatted,
        "ai_message": ai_message,
        "user": current_user
    })

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"error": None})

@app.post("/login")
async def login(
    request: Request, 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse(request, "login.html", {
            "error": "Invalid email or password"
        })
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, 
        expires_delta=access_token_expires
    )
    
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response

@app.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    db = next(get_db())
    company = db.query(Company).filter(Company.id == current_user.company_id).first()
    settings = db.query(CompanySettings).filter(CompanySettings.company_id == current_user.company_id).first()
    
    if not settings:
        settings = CompanySettings(company_id=current_user.company_id, test_mode=True)
        db.add(settings)
        db.commit()
    
    return templates.TemplateResponse(request, "settings.html", {
        "company": company,
        "settings": settings,
        "user": current_user
    })

@app.post("/settings")
async def update_settings(
    request: Request,
    github_org: str = Form(...),
    slack_channel: str = Form(...),
    test_mode: bool = Form(False),
    auto_recover: bool = Form(False),
    current_user: User = Depends(get_current_user_from_cookie)
):
    db = next(get_db())
    company = db.query(Company).filter(Company.id == current_user.company_id).first()
    if not company:
        return RedirectResponse(url="/settings", status_code=303)
    
    # Type ignore for SQLAlchemy assignments
    company.github_org = github_org  # type: ignore
    company.slack_channel = slack_channel  # type: ignore
    
    settings = db.query(CompanySettings).filter(CompanySettings.company_id == current_user.company_id).first()
    if not settings:
        settings = CompanySettings(company_id=current_user.company_id)
        db.add(settings)
    
    settings.test_mode = test_mode  # type: ignore
    settings.auto_recover_enabled = auto_recover  # type: ignore
    
    db.commit()
    return RedirectResponse(url="/settings", status_code=303)

@app.get("/download/report")
async def download_report(current_user: User = Depends(get_current_user_from_cookie)):
    ghost_list = ghost_hunter.find_ghosts("employees.csv")
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Team", "Monthly Salary", "Days Since Code", "Days Since Slack", "Ghost Score", "Status"])
    
    for person in ghost_list:
        writer.writerow([
            person['name'],
            person['team'],
            person['salary'],
            person['github_gap_days'],
            person['slack_gap_days'],
            person['score'],
            person['status']
        ])
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=ghost_report.csv"}
    )

@app.post("/recover/{name}")
async def recover_ghost(
    name: str, 
    current_user: User = Depends(get_current_user_from_cookie)
):
    ghost_list = ghost_hunter.find_ghosts("employees.csv")
    
    target = None
    for person in ghost_list:
        if person['name'].lower() == name.lower():
            target = person
            break
    
    if not target:
        return JSONResponse(status_code=404, content={"success": False, "message": f"Ghost '{name}' not found"})
    
    if target['score'] < 60:
        return JSONResponse(status_code=400, content={"success": False, "message": f"{name} is not a ghost"})
    
    success, github_msg, slack_msg = auto_recover.auto_recover_ghost(target)
    
    return {
        "success": success,
        "message": f"Recovery for {name}: {github_msg} | {slack_msg}",
        "github": github_msg,
        "slack": slack_msg
    }