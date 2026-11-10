from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler

from app.database import SessionLocal
from app import models
from app.monitor import check_website
from app.email_alerts import send_alert


def run_monitoring_cycle():

    db = SessionLocal()

    try:
        websites = (
            db.query(models.MonitoredWebsite)
            .filter(models.MonitoredWebsite.is_active == True)
            .all()
        )

        for website in websites:

            result = check_website(website.url)

            new_check = models.WebsiteCheck(
                url=result["url"],
                status=result["status"],
                status_code=result["status_code"],
                response_time_ms=result["response_time_ms"],
                error=result["error"]
            )

            db.add(new_check)

            open_incident = (
                db.query(models.Incident)
                .filter(
                    models.Incident.website_id == website.id,
                    models.Incident.status == "OPEN"
                )
                .first()
            )

            if result["status"] == "DOWN" and open_incident is None:

                incident = models.Incident(
                    website_id=website.id,
                    url=website.url,
                    status="OPEN"
                )

                db.add(incident)

                print(f"INCIDENT CREATED: {website.url}")

                db.flush()

                send_alert(
                    url=website.url,
                    status="DOWN",
                    error=result["error"]
                )

            elif result["status"] == "UP" and open_incident is not None:

                open_incident.status = "RESOLVED"
                open_incident.resolved_at = datetime.now(timezone.utc)

                print(f"INCIDENT RESOLVED: {website.url}")

        db.commit()

    except Exception as error:
        db.rollback()
        print(f"Monitoring error: {error}")

    finally:
        db.close()


scheduler = BackgroundScheduler()

scheduler.add_job(
    run_monitoring_cycle,
    trigger="interval",
    seconds=60,
    id="website_monitoring",
    replace_existing=True
)