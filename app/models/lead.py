# app/models/lead.py
from sqlalchemy import Column, String, DateTime, Enum as SAEnum
import enum
from datetime import datetime, timezone

# ✅ CORRECT: Import Base from database.py
from app.database import Base

class LeadStatus(str, enum.Enum):
    captured = "captured"
    enriched = "enriched"
    notified = "notified"
    converted = "converted"

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=True)
    area_of_interest = Column(String, nullable=False)
    source = Column(String, nullable=False)
    status = Column(SAEnum(LeadStatus), default=LeadStatus.captured)
    workflow_run_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))