from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ErrorType(str, Enum):
    validation_error = "validation_error"
    duplicate_entry = "duplicate_entry"
    api_failure = "api_failure"
    timeout = "timeout"
    manual_intervention_required = "manual_intervention_required"

class ResolutionStatus(str, Enum):
    unresolved = "unresolved"
    resolved = "resolved"
    ignored = "ignored"

class ErrorLogBase(BaseModel):
    workflow_type: str
    workflow_run_id: int
    step_name: str
    error_type: ErrorType
    error_message: str
    http_status_code: Optional[int] = None

class ErrorLogCreate(ErrorLogBase):
    pass

class ErrorLogResponse(ErrorLogBase):
    id: int
    timestamp: datetime
    resolution_status: ResolutionStatus
    resolution_note: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None

    class Config:
        from_attributes = True

class ErrorLogUpdate(BaseModel):
    resolution_status: ResolutionStatus
    resolution_note: Optional[str] = None