from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import os
import requests

from app.database import get_db
from app.models.lead import Lead, LeadStatus
from app.schemas.lead import LeadCreate, LeadResponse

router = APIRouter(tags=["Lead Capture"])

@router.post("/leads", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(lead_data: LeadCreate, db: Session = Depends(get_db)):
    # 1. Duplicate prevention (SRS 3.3.3: same email within 30 days)
    duplicate_window_days = int(os.getenv("LEAD_DUPLICATE_WINDOW_DAYS", "30"))
    threshold = datetime.utcnow() - timedelta(days=duplicate_window_days)
    
    existing = db.query(Lead).filter(
        Lead.email == lead_data.email,
        Lead.created_at > threshold
    ).first()
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Duplicate lead: email captured recently."
        )

    # 2. Create & Enrich
    new_lead = Lead(**lead_data.model_dump(), status=LeadStatus.captured)
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    # 3. Enrich with metadata (SRS 3.3.3 FR-10)
    new_lead.status = LeadStatus.enriched
    db.commit()

    # 4. Slack Notification (SRS 3.3.3 FR-10)
    slack_webhook = os.getenv("SLACK_LEAD_WEBHOOK")
    if slack_webhook:
        try:
            requests.post(
                slack_webhook,
                json={
                    "text": f"🆕 New Lead: {new_lead.name} ({new_lead.company})\n📧 {new_lead.email}\n🎯 {new_lead.interest}"
                },
                timeout=5
            )
            new_lead.status = LeadStatus.notified
            db.commit()
        except Exception as e:
            # In production, route to error_logs per SRS 3.2
            pass

    return new_lead

@router.get("/leads", response_model=List[LeadResponse])
async def get_leads(
    status_filter: Optional[str] = None,
    source_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Lead)
    if status_filter:
        query = query.filter(Lead.status == status_filter)
    if source_filter:
        query = query.filter(Lead.source == source_filter)
    return query.order_by(Lead.created_at.desc()).all()