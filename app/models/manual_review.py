from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base

class ReviewStatus(PyEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ManualReview(Base):
    __tablename__ = "manual_reviews"

    id = Column(Integer, primary_key=True, index=True)
    error_log_id = Column(Integer, ForeignKey("error_logs.id"), unique=True, nullable=False)
    source_workflow_type = Column(String, nullable=False)
    source_record_id = Column(Integer, nullable=False)
    assigned_reviewer = Column(String, nullable=True)
    review_status = Column(Enum(ReviewStatus), default=ReviewStatus.pending)
    reviewer_notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    # Relationship to Error Log
    error_log = relationship("ErrorLog", back_populates="manual_review")