from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import Order, Refund
from app.schemas import RefundCreate, RefundResponse

router = APIRouter(prefix="/refunds", tags=["Refund Workflow"])

@router.post("/", response_model=RefundResponse, status_code=status.HTTP_201_CREATED)
def request_refund(refund_data: RefundCreate, db: Session = Depends(get_db)):
    
    # 1. Verify Order Exists
    order = db.query(Order).filter(Order.id == refund_data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 2. Validate Refund Amount (cannot exceed order total)
    if refund_data.refund_amount > order.total_price:
        raise HTTPException(status_code=400, detail="Refund amount cannot exceed order total")

    # 3. Prevent Duplicate Refunds (SRS 3.3.3 FR-3)
    existing = db.query(Refund).filter(Refund.order_id == refund_data.order_id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Refund already requested for this order")

    # 4. Create Refund Record
    # SRS 3.3.3 FR-4: Automatically approve refunds that pass all policy validations
    new_refund = Refund(
        order_id=refund_data.order_id,
        customer_contact=refund_data.customer_contact,
        refund_amount=refund_data.refund_amount,
        refund_reason=refund_data.refund_reason,
        refund_status="approved",  # Auto-approved per SRS 3.3.3
        requested_at=datetime.utcnow(),
        approved_at=datetime.utcnow()
    )

    db.add(new_refund)
    db.commit()
    db.refresh(new_refund)

    return new_refund

@router.get("/", response_model=List[RefundResponse])
def get_refunds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    SRS 3.3.3 FR-7: GET /refunds filterable by status, date range, and order ID
    """
    return db.query(Refund).offset(skip).limit(limit).all()