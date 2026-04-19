from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import SessionLocal
from app.models.error_log import ErrorLog, ErrorType, ResolutionStatus
from app.schemas.error_log import ErrorLogCreate, ErrorLogResponse, ErrorLogUpdate

router = APIRouter(prefix="/error-logs", tags=["Error Detection & Logging"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[ErrorLogResponse])
async def get_error_logs(
    workflow_type: Optional[str] = Query(None, description="Filter by workflow type (order, refund, lead, email)"),
    error_type: Optional[str] = Query(None, description="Filter by error category"),
    resolution_status: Optional[str] = Query(None, description="Filter by resolution status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get error logs with filtering (SRS 3.2.3 #4)"""
    query = db.query(ErrorLog)
    
    if workflow_type:
        query = query.filter(ErrorLog.workflow_type == workflow_type)
    if error_type:
        query = query.filter(ErrorLog.error_type == error_type)
    if resolution_status:
        query = query.filter(ErrorLog.resolution_status == resolution_status)
        
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=ErrorLogResponse, status_code=201)
async def create_error_log(error: ErrorLogCreate, db: Session = Depends(get_db)):
    """Log a new workflow error (SRS 3.2.3 #2, #3)"""
    db_error = ErrorLog(**error.dict(), resolution_status=ResolutionStatus.unresolved)
    db.add(db_error)
    db.commit()
    db.refresh(db_error)
    
    # TODO: Trigger alert notification here (SRS 3.2.3 #5)
    return db_error

@router.patch("/{error_id}", response_model=ErrorLogResponse)
async def update_error_log(error_id: int, update: ErrorLogUpdate, db: Session = Depends(get_db)):
    """Mark error as resolved (SRS 3.2.3 #6)"""
    db_error = db.query(ErrorLog).filter(ErrorLog.id == error_id).first()
    if not db_error:
        raise HTTPException(status_code=404, detail="Error log not found")
        
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_error, key, value)
        
    db_error.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(db_error)
    return db_error