# app/schemas/scheduled_email.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ScheduledEmailCreate(BaseModel):
    recipient_name: str
    recipient_email: EmailStr
    send_date: datetime
    email_subject: str
    email_body: str

class ScheduledEmailResponse(BaseModel):
    id: int
    recipient_name: str
    recipient_email: str
    send_date: datetime
    email_subject: str
    email_body: str
    sent_status: bool
    sent_at: Optional[datetime]
    error_message: Optional[str]
    workflow_run_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ScheduledEmailLog(BaseModel):
    """For logging send attempts"""
    recipient_email: str
    send_date: datetime
    dispatch_status: str  # "success" or "failed"
    timestamp: datetime
    error_message: Optional[str] = None