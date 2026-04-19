from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base

class ErrorType(PyEnum):
    validation_error = "validation_error"
    duplicate_entry = "duplicate_entry"
    api_failure = "api_failure"
    timeout = "timeout"
    manual_intervention_required = "manual_intervention_required"

class ResolutionStatus(PyEnum):
    unresolved = "unresolved"
    resolved = "resolved"
    ignored = "ignored"

class ErrorLog(Base):
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_type = Column(String, nullable=False)  # "order", "refund", "lead", "email"
    workflow_run_id = Column(Integer, nullable=False)
    step_name = Column(String, nullable=False)
    error_type = Column(Enum(ErrorType), nullable=False)
    error_message = Column(String, nullable=False)
    http_status_code = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    resolution_status = Column(Enum(ResolutionStatus), default=ResolutionStatus.unresolved)
    resolution_note = Column(String, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(String, nullable=True)

    # Relationship to Manual Review
    manual_review = relationship("ManualReview", back_populates="error_log", uselist=False)