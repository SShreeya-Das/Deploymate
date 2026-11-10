from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean,ForeignKey
from datetime import datetime, timezone

from app.database import Base


class WebsiteCheck(Base):

    __tablename__ = "website_checks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    status = Column(String, nullable=False)
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Float, nullable=True)
    error = Column(String, nullable=True)

    checked_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )


class MonitoredWebsite(Base):

    __tablename__ = "monitored_websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    interval_seconds = Column(Integer, default=60)

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
class Incident(Base):

    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("monitored_websites.id"))
    url = Column(String, nullable=False)
    status = Column(String, default="OPEN")
    started_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    resolved_at = Column(DateTime, nullable=True)    