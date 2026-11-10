import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_alert(url: str, status: str, error: str = None):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    alert_email = os.getenv("ALERT_EMAIL")

    if not all([smtp_host, smtp_user, smtp_password, alert_email]):
        print("Email alert configuration is incomplete.")
        return False

    message = EmailMessage()

    message["Subject"] = f"DeployMate Alert: {url} is {status}"
    message["From"] = smtp_user
    message["To"] = alert_email

    message.set_content(
        f"""
DeployMate Website Monitoring Alert

Website: {url}
Current Status: {status}
Error: {error or "None"}

Please investigate this website.
"""
    )

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)

        print(f"Email alert sent for {url}")
        return True

    except Exception as exception:
        print(f"Email alert failed: {type(exception).__name__}")
        return False