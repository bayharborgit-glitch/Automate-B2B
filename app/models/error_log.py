# app/models/error_log.py
from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

# ✅ CRITICAL: Import Base from database.py (DON'T create a new one!)
from app.database import Base

class ErrorType(str, PyEnum):
    """Error categories as defined in SRS Section 3.2.3"""
    validation_error = "validation_error"
    duplicate_entry = "duplicate_entry"
    api_failure = "api_failure"
    timeout = "timeout"
    manual_intervention_required = "manual_intervention_required"

class ResolutionStatus(str, PyEnum):
    """Resolution states for error logs"""
    unresolved = "unresolved"
    resolved = "resolved"
    escalated = "escalated"

class ErrorLog(Base):
    """
    Error log model - SRS Section 3.2.3
    Tracks every workflow step failure with full context for audit and manual review.
    """
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_type = Column(String, nullable=False)  # e.g., "order", "refund", "lead", "scheduled_email"
    workflow_run_id = Column(String, nullable=False, index=True)
    step_name = Column(String, nullable=False)  # e.g., "validate_order", "send_slack", "check_inventory"
    error_type = Column(SAEnum(ErrorType), nullable=False)
    error_message = Column(String, nullable=False)
    http_status_code = Column(Integer, nullable=True)
    resolution_status = Column(SAEnum(ResolutionStatus), default=ResolutionStatus.unresolved)
    resolution_note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
 # Relationship to ManualReview (one error can have one manual review)
    manual_review = relationship("ManualReview", back_populates="error_log", uselist=False)