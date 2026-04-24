# app/models/scheduled_email.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class ScheduledEmail(Base):
    __tablename__ = "scheduled_emails"

    id = Column(Integer, primary_key=True, index=True)
    recipient_name = Column(String, nullable=False)
    recipient_email = Column(String, nullable=False)
    send_date = Column(DateTime, nullable=False)
    email_subject = Column(String, nullable=False)
    email_body = Column(Text, nullable=False)
    sent_status = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)
    workflow_run_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)