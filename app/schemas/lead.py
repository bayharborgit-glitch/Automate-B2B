from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class LeadCreate(BaseModel):
    name: str
    company: str
    email: EmailStr
    phone: Optional[str] = None
    interest: str
    source: str

class LeadResponse(BaseModel):
    id: int
    name: str
    company: str
    email: str
    phone: Optional[str]
    interest: str
    source: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True