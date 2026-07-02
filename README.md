# 👻 Ghost Hunter - AI-Powered Employee Monitoring

**Ghost Hunter** is a production-ready SaaS platform that uses AI to detect and automatically recover "ghost employees" – inactive users who are still costing your company money through unused software licenses.

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://python.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.23-9C3A3A)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

Ghost Hunter solves a critical business problem: **companies waste 50-60% of their SaaS spend on unused licenses.** This platform:

1. **Detects** ghost employees by analyzing GitHub activity and Slack communication
2. **Calculates** financial impact (monthly savings opportunity)
3. **Recovers** licenses automatically with a single click
4. **Generates** AI-powered reports and recommendations

### The Problem We Solve

| Metric | Industry Average |
|--------|------------------|
| SaaS License Waste | 54.8% |
| Annual Waste per Company | $18M - $21M |
| Waste Growth Rate | 14.2% YoY |

**Source:** Zylo 2025 SaaS Management Index

---

## ✨ Features

### Core Features

| Feature | Description |
|---------|-------------|
| **🔍 Ghost Detection** | Analyzes GitHub commits and Slack activity to identify inactive users |
| **🤖 AI Scoring** | Machine learning algorithm calculates a "Ghost Score" (0-100) |
| **💰 Savings Calculator** | Shows real-time monthly savings opportunities |
| **⚡ Auto-Recover** | One-click removal of ghosts from GitHub with Slack notifications |
| **📊 CSV Reports** | Export employee audit reports for meetings |
| **🔐 Multi-Tenant** | Each company has isolated data and settings |
| **👤 User Authentication** | Secure JWT-based login with cookie storage |
| **🎨 Modern UI** | Bootstrap 5 dashboard with dark mode support |

### AI Features

| Feature | Description |
|---------|-------------|
| **AI Roast** | OpenRouter-powered witty CFO-style roast for each ghost |
| **Smart Fallback** | Intelligent fallback when APIs are unavailable |
| **Auto-Selection** | Automatic selection of best available AI model |

### Integration Support

| Integration | Status | Details |
|-------------|--------|---------|
| **GitHub API** | ✅ Supported | Fetches last commit date for each user |
| **Slack API** | ✅ Supported | Fetches last activity date (or uses smart fallback) |
| **OpenRouter AI** | ✅ Supported | AI-powered ghost roasts (free tier available) |

---

## 🛠️ Tech Stack

### Backend

| Technology | Purpose |
|------------|---------|
| **FastAPI** | Web framework (async, high-performance) |
| **Python 3.11+** | Core language |
| **SQLAlchemy** | ORM for database operations |
| **SQLite / PostgreSQL** | Database (SQLite for development, PostgreSQL for production) |
| **JWT** | Authentication with secure cookies |
| **bcrypt** | Password hashing |

### APIs & External Services

| Service | Purpose |
|---------|---------|
| **GitHub API** | User activity data |
| **Slack API** | User presence & notifications |
| **OpenRouter API** | AI-generated content (free tier) |

### Frontend

| Technology | Purpose |
|------------|---------|
| **Jinja2** | Server-side HTML templating |
| **Bootstrap 5** | Responsive UI framework |
| **Chart.js** | Data visualization (optional) |
| **Font Awesome** | Icons |

---

## 📸 Screenshots

### Dashboard
*[Add a screenshot of your dashboard here]*

### Employee Audit Report
*[Add a screenshot of the employee table here]*

### Settings Page
*[Add a screenshot of the settings page here]*

---

## 🚀 Installation

### Prerequisites

- Python 3.11 or higher
- Git
- GitHub account with organization
- Slack workspace with admin access
- OpenRouter API key (free)

### Step 1: Clone the Repository

```bash
git clone https://github.com/edubio228/ghost-hunter-mvp.git
cd ghost-hunter-mvp


Step 2: Create Virtual Environment
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
Step 4: Set Up Environment Variables
Create a .env file in the root directory:

env
SECRET_KEY=your-secure-random-key-here
GITHUB_TOKEN=ghp_your_actual_token
SLACK_BOT_TOKEN=xoxb_your_actual_token
OPENROUTER_API_KEY=sk-or-v1_your_actual_key
GITHUB_ORG=your-github-org-name
SLACK_NOTIFICATION_CHANNEL=CXXXXXXXXXX
TEST_MODE=True
DATABASE_URL=sqlite:///./ghost_hunter.db
Step 5: Generate a Secure Secret Key
bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
Copy the output and paste it as your SECRET_KEY in .env.

⚙️ Configuration
GitHub Token Setup
Go to https://github.com/settings/tokens

Generate a new classic token

Scopes required: repo (or public_repo for public repos only)

admin:org – for auto-recover functionality

Slack Bot Setup
Go to https://api.slack.com/apps

Create a new app "From Scratch"

Under "OAuth & Permissions", add these scopes:

users:read

channels:history

chat:write

Install the app to your workspace

Copy the Bot User OAuth Token (starts with xoxb-)

OpenRouter API Setup
Go to https://openrouter.ai/keys

Sign up (free)

Generate an API key

Copy the key (starts with sk-or-v1-)

🏃 Running the App
Development Mode
bash
python run.py
The app will be available at: http://localhost:8000

📡 API Endpoints
Method	Endpoint	Description
GET	/	Dashboard (authenticated)
GET	/login	Login page
POST	/login	Handle login
GET	/logout	Logout user
GET	/settings	Company settings page
POST	/settings	Update settings
GET	/download/report	Download CSV report
POST	/recover/{name}	Auto-recover a ghost
🚢 Deployment
Option 1: Render.com (Recommended)
Push your code to GitHub

Go to https://render.com

Click "New +" → "Web Service"

Connect your GitHub repository

Configure:

Build Command: pip install -r requirements.txt

Start Command: uvicorn app.main:app --host 0.0.0.0 --port 10000

Add all environment variables from your .env file

Click "Create Web Service"

Option 2: Railway.app
Push your code to GitHub

Go to https://railway.app

Click "New Project" → "Deploy from GitHub repo"

Connect your repository

Add all environment variables

Deploy!

Option 3: Docker
dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
🔒 Security Checklist
Item	Status
.env in .gitignore	✅
SECRET_KEY changed	⚠️ Required
admin@demo.com password changed	⚠️ Required
GitHub token with minimal permissions	✅
HTTPS enabled in production	⚠️ Required
Rate limiting implemented	⚠️ Recommended
🧪 Testing
Test Auto-Recover Safely
Create a dummy GitHub user

Invite them to your organization

Add them to employees.csv

Set TEST_MODE=True in .env

Click "Recover" – it will simulate the action

When ready, set TEST_MODE=False for real action

🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

🙏 Acknowledgments
FastAPI – For the beautiful async framework

OpenRouter – For providing free AI API access

GitHub – For the incredible API

Slack – For the collaboration platform

📞 Support
For support, please open an issue on GitHub or contact the maintainer.

Built with ❤️ by the Ghost Hunter Team

📚 Additional Resources
FastAPI Documentation

GitHub API Documentation

Slack API Documentation

OpenRouter Documentation

🏆 Contributors
Name	Role
Emmanuel Edubio	Lead Developer


⭐ Star this repository if you find it useful! ⭐


