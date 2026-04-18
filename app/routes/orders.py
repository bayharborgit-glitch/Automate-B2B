from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.order import Order, WorkflowStatus
from app.schemas.order import OrderCreate, OrderResponse
from typing import List, Optional

router = APIRouter(prefix="/orders", tags=["orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    existing = db.query(Order).filter(
        Order.customer_contact == order.customer_contact,
        Order.product_details == order.product_details
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Duplicate order detected")
    
    db_order = Order(**order.model_dump(), payment_status="pending", workflow_status=WorkflowStatus.received)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@router.get("/", response_model=List[OrderResponse])
async def get_orders(status: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Order)
    if status:
        query = query.filter(Order.workflow_status == status)
    return query.all()

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order