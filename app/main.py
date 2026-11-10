from fastapi.responses import HTMLResponse 
from pathlib import Path
from app.email_alerts import send_alert
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from contextlib import asynccontextmanager

from app.monitor import check_website
from app.database import engine, Base, SessionLocal
from app import models
from app.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="DeployMate",
    description="Application uptime and performance monitoring platform",
    version="0.1.0",
    lifespan=lifespan
)


class MonitorRequest(BaseModel):
    url: HttpUrl


class WebsiteCreate(BaseModel):
    url: HttpUrl


@app.get("/")
def home():
    return {
        "message": "Welcome to DeployMate!",
        "status": "running"
    }

@app.post("/monitor")
def monitor_website(request: MonitorRequest):

    db = SessionLocal()

    try:
        result = check_website(str(request.url))

        new_check = models.WebsiteCheck(
            url=result["url"],
            status=result["status"],
            status_code=result["status_code"],
            response_time_ms=result["response_time_ms"],
            error=result["error"]
        )

        db.add(new_check)
        db.commit()
        db.refresh(new_check)

        result["id"] = new_check.id

        return result

    finally:
        db.close()
@app.get("/history")
def get_monitoring_history():

    db = SessionLocal()

    try:
        records = (
            db.query(models.WebsiteCheck)
            .order_by(models.WebsiteCheck.checked_at.desc())
            .all()
        )

        return records

    finally:
        db.close()       
@app.get("/history")
def get_monitoring_history(url: HttpUrl | None = None):

    db = SessionLocal()

    try:
        query = db.query(models.WebsiteCheck)

        if url:
            query = query.filter(
                models.WebsiteCheck.url == str(url)
            )

        records = (
            query
            .order_by(models.WebsiteCheck.checked_at.desc())
            .all()
        )

        return records

    finally:
        db.close()
@app.post("/websites")
def add_website(request: WebsiteCreate):

    db = SessionLocal()

    try:
        url = str(request.url)

        existing = (
            db.query(models.MonitoredWebsite)
            .filter(models.MonitoredWebsite.url == url)
            .first()
        )

        if existing:
            return {
                "message": "Website already registered",
                "id": existing.id
            }

        new_website = models.MonitoredWebsite(
            url=url,
            is_active=True,
            interval_seconds=60
        )

        db.add(new_website)
        db.commit()
        db.refresh(new_website)

        return {
            "message": "Website registered successfully",
            "id": new_website.id,
            "url": new_website.url,
            "status": "Monitoring enabled"
        }

    finally:
        db.close()        

@app.get("/websites")
def get_websites():

    db = SessionLocal()

    try:
        websites = (
            db.query(models.MonitoredWebsite)
            .order_by(models.MonitoredWebsite.id.desc())
            .all()
        )

        return [
            {
                "id": website.id,
                "url": website.url,
                "is_active": website.is_active,
                "interval_seconds": website.interval_seconds,
                "created_at": website.created_at
            }
            for website in websites
        ]

    finally:
        db.close()
@app.get("/incidents")
def get_incidents():

    db = SessionLocal()

    try:
        incidents = (
            db.query(models.Incident)
            .order_by(models.Incident.started_at.desc())
            .all()
        )

        return [
            {
                "id": incident.id,
                "website_id": incident.website_id,
                "url": incident.url,
                "status": incident.status,
                "started_at": incident.started_at,
                "resolved_at": incident.resolved_at
            }
            for incident in incidents
        ]

    finally:
        db.close()  
@app.post("/test-email")
def test_email():

    success = send_alert(
        url="https://example.com",
        status="TEST"
    )

    if success:
        return {"message": "Test email sent successfully!"}

    return {"message": "Email sending failed. Check terminal logs."}   
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    dashboard_path = Path(__file__).parent / "dashboard.html"

    return dashboard_path.read_text(encoding="utf-8")               