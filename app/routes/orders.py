from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.order import Order, WorkflowStatus
from app.schemas.order import OrderCreate, OrderResponse
from typing import List, Optional  # ← Added Optional here

router = APIRouter(prefix="/orders", tags=["orders"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate):
    """Capture a new order from website (SRS 3.1.3)"""
    db = SessionLocal()
    
    # Check for duplicates (simple check)
    existing = db.query(Order).filter(
        Order.customer_contact == order.customer_contact,
        Order.product_details == order.product_details
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Duplicate order detected")
    
    # Create new order
    db_order = Order(
        **order.dict(),
        payment_status="pending",
        workflow_status=WorkflowStatus.received
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return db_order

@router.get("/", response_model=List[OrderResponse])
async def get_orders(status: Optional[str] = None):
    """Get all orders, filterable by status"""
    db = SessionLocal()
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.workflow_status == status)
    
    return query.all()

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    """Get specific order by ID"""
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return order