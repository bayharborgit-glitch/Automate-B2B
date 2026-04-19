from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ReviewStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ManualReviewBase(BaseModel):
    error_log_id: int
    source_workflow_type: str
    source_record_id: int
    assigned_reviewer: Optional[str] = None

class ManualReviewCreate(ManualReviewBase):
    pass

class ManualReviewResponse(ManualReviewBase):
    id: int
    review_status: ReviewStatus
    reviewer_notes: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ManualReviewAction(BaseModel):
    reviewer_notes: Optional[str] = None