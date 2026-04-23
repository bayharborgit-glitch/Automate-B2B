from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.lead_service import create_lead
from app.models.lead import Lead, LeadStatus

router = APIRouter(prefix="/leads", tags=["Lead Capture"])

@router.post("/", response_model=LeadResponse, status_code=201)
def capture_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Capture a new lead from web form. Validates, checks duplicates, enriches, notifies Slack."""
    return create_lead(db, lead)

@router.get("/", response_model=List[LeadResponse])
def list_leads(
    status: Optional[LeadStatus] = Query(None),
    source: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """List leads with optional filters."""
    query = db.query(Lead)
    if status: query = query.filter(Lead.status == status)
    if source: query = query.filter(Lead.source == source)
    if start_date: query = query.filter(Lead.created_at >= start_date)
    if end_date: query = query.filter(Lead.created_at <= end_date)
    return query.order_by(Lead.created_at.desc()).all()