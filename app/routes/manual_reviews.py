from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import SessionLocal
from app.models.manual_review import ManualReview, ReviewStatus
from app.schemas.manual_review import ManualReviewResponse, ManualReviewAction

router = APIRouter(prefix="/manual-reviews", tags=["Manual Review Queue"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# TODO: Replace with real RBAC dependency from SRS 3.2.3 #3
def require_manager_or_admin():
    return {"role": "admin", "user_id": "test-admin"}

@router.get("/", response_model=List[ManualReviewResponse])
async def get_manual_reviews(
    status: Optional[str] = Query(None, description="Filter by review status"),
    source_workflow: Optional[str] = Query(None, description="Filter by source workflow type"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get manual review queue (SRS 3.2.3 #2)"""
    query = db.query(ManualReview)
    if status:
        query = query.filter(ManualReview.review_status == status)
    if source_workflow:
        query = query.filter(ManualReview.source_workflow_type == source_workflow)
        
    return query.order_by(ManualReview.created_at.desc()).offset(skip).limit(limit).all()

@router.post("/{review_id}/approve", response_model=ManualReviewResponse)
async def approve_review(
    review_id: int,
    action: ManualReviewAction,
    db: Session = Depends(get_db),
    user = Depends(require_manager_or_admin)  # RBAC enforcement
):
    """Approve paused workflow (SRS 3.2.3 #6, #8)"""
    review = db.query(ManualReview).filter(ManualReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
        
    review.review_status = ReviewStatus.approved
    review.reviewer_notes = action.reviewer_notes
    review.resolved_at = datetime.utcnow()
    review.assigned_reviewer = user.get("user_id")
    
    db.commit()
    db.refresh(review)
    
    # TODO: Signal originating workflow to resume (SRS 3.2.3 #6)
    return review

@router.post("/{review_id}/reject", response_model=ManualReviewResponse)
async def reject_review(
    review_id: int,
    action: ManualReviewAction,
    db: Session = Depends(get_db),
    user = Depends(require_manager_or_admin)  # RBAC enforcement
):
    """Reject paused workflow (SRS 3.2.3 #7, #8)"""
    review = db.query(ManualReview).filter(ManualReview.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
        
    review.review_status = ReviewStatus.rejected
    review.reviewer_notes = action.reviewer_notes
    review.resolved_at = datetime.utcnow()
    review.assigned_reviewer = user.get("user_id")
    
    db.commit()
    db.refresh(review)
    
    # TODO: Signal originating workflow to cancel (SRS 3.2.3 #7)
    return review