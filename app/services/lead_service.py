# app/services/lead_service.py
from sqlalchemy.orm import Session
from app.models.lead import Lead, LeadStatus
from app.schemas.lead import LeadCreate
from uuid import uuid4
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)
DUPLICATE_WINDOW_HOURS = 24

def create_lead(db: Session, lead_data: LeadCreate):  # ✅ FIXED: colon added, param named lead_data
    """
    Lead Capture Workflow (SRS Section 3.3):
    1. Check for duplicates (same email within 24h)
    2. Create lead record with 'captured' status
    3. Enrich with metadata (status → 'enriched')
    4. Send Slack notification (status → 'notified')
    5. Return lead with workflow_run_id
    """
    
    # 1. Duplicate Check
    cutoff = datetime.now(timezone.utc) - timedelta(hours=DUPLICATE_WINDOW_HOURS)
    existing = db.query(Lead).filter(
        Lead.email == lead_data.email,
        Lead.created_at >= cutoff
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Duplicate lead: {lead_data.email} already captured within {DUPLICATE_WINDOW_HOURS}h window"
        )
    
    # 2. Create Lead Record
    workflow_id = str(uuid4())
    db_lead = Lead(
        id=str(uuid4()),
        workflow_run_id=workflow_id,
        name=lead_data.name,
        company=lead_data.company,
        email=lead_data.email,
        phone=lead_data.phone,
        area_of_interest=lead_data.area_of_interest,
        source=lead_data.source,
        status=LeadStatus.captured,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    # 3. Enrich Lead (add metadata)
    db_lead.status = LeadStatus.enriched
    db_lead.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_lead)
    
    # 4. Send Slack Notification (mock)
    try:
        send_slack_notification(db_lead)
        db_lead.status = LeadStatus.notified
        db_lead.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_lead)
    except Exception as e:
        # Hook into Error Detection & Manual Review (SRS Section 3.2)
        logger.error(f"Slack notification failed for lead {db_lead.id}: {e}")
        # TODO: Call create_manual_review(db, db_lead.id, "api_failure", str(e))
    
    return db_lead

def send_slack_notification(lead: Lead):
    """Mock Slack notification - replace with real webhook later"""
    logger.info(f"[SLACK] New Lead: {lead.name} | {lead.email} | {lead.area_of_interest}")
    # Real implementation: requests.post(SLACK_WEBHOOK_URL, json={...})
    pass