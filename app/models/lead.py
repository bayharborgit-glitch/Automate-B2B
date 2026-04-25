from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum
from sqlalchemy.sql import func
from app.database import Base
import enum

class LeadStatus(str, enum.Enum):
    captured = "captured"
    enriched = "enriched"
    notified = "notified"
    converted = "converted"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    interest = Column(String, nullable=False)
    source = Column(String, nullable=False)  # e.g., "website_form", "linkedin"
    status = Column(SAEnum(LeadStatus), default=LeadStatus.captured, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())