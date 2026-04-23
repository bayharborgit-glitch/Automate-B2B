from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.lead import LeadStatus

class LeadCreate(BaseModel):
    name: str = Field(..., min_length=2)
    company: str
    email: EmailStr
    phone: Optional[str] = None
    area_of_interest: str
    source: str

class LeadResponse(BaseModel):
    id: str
    name: str
    company: str
    email: EmailStr
    phone: Optional[str]
    area_of_interest: str
    source: str
    status: LeadStatus
    workflow_run_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True