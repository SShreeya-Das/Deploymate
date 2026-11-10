DeployMate 🚀

Website Monitoring & Incident Management Platform

DeployMate is a Python-based website monitoring platform that checks website availability, tracks response times, records monitoring history, and generates incident alerts when a website goes down.

✨ Features

- Website Monitoring: Monitor registered websites automatically.
- Availability Tracking: Identify websites as UP or DOWN based on HTTP responses.
- Performance Analytics: Track average, fastest, and slowest response times.
- Incident Management: Automatically create and resolve incidents when website availability changes.
- Email Notifications: Receive email alerts when a monitored website goes down.
- Interactive Dashboard: View website status, monitoring history, incidents, and performance analytics.
- Automated Scheduling: Run monitoring cycles in the background.

🛠️ Tech Stack

Technology| Purpose
Python| Core programming language
FastAPI| Backend API
SQLAlchemy| Database ORM
SQLite| Data persistence
HTTPX| HTTP monitoring requests
APScheduler| Background scheduling
Chart.js| Dashboard analytics
HTML & CSS| Dashboard interface
SMTP| Email notifications
Pytest| Automated testing

📂 Project Structure

DeployMate/
├── app/
│   ├── main.py
│   ├── monitor.py
│   ├── scheduler.py
│   ├── database.py
│   ├── models.py
│   ├── email_alerts.py
│   └── dashboard.html
├── tests/
│   └── test_monitor.py
├── requirements.txt
├── .gitignore
└── README.md

⚙️ Installation & Setup

1. Clone the repository

git clone https://github.com/SShreeya-Das/Deploymate.git
cd Deploymate

2. Create a virtual environment

python -m venv .venv

Activate it on Windows:

.\.venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Configure email notifications

Create a ".env" file in the project root:

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
ALERT_EMAIL=your_email@gmail.com

Use a Gmail App Password rather than your regular account password.

5. Run the application

uvicorn app.main:app --reload

🌐 Access the Application

- Dashboard: http://127.0.0.1:8000/dashboard
- API Documentation: http://127.0.0.1:8000/docs
- Health Check: http://127.0.0.1:8000/

🧪 Run Tests

python -m pytest -v

🔌 API Endpoints

## 🔌 API Endpoints

| Method | Endpoint | Description |
|:---|:---|:---|
| GET | `/` | Application health check |
| POST | `/monitor` | Check a website manually |
| POST | `/websites` | Register a website |
| GET | `/websites` | List monitored websites |
| GET | `/history` | Retrieve monitoring history |
| GET | `/incidents` | Retrieve incident history |
| POST | `/test-email` | Test email notifications |
| GET | `/dashboard` | Open monitoring dashboard |
🔮 Future Improvements

- Advanced URL and SSRF protection
- User authentication and role-based access
- Docker containerisation
- Cloud deployment
- Configurable monitoring intervals
- Advanced alerting and reporting

👩‍💻 Author

Shreeya Swarupa Das

- GitHub: "@SShreeya-Das" (https://github.com/SShreeya-Das)
- LinkedIn: "Connect with me"www.linkedin.com/in/shreeya-swarupa-das-660689289



---

DeployMate is a portfolio project developed to explore backend engineering, website reliability monitoring, automation, and incident management.
