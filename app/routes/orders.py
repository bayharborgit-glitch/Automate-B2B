from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.order import Order, WorkflowStatus
from app.schemas.order import OrderCreate, OrderResponse
from typing import List, Optional

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate):
    db = SessionLocal()
    try:
        # Check for duplicate
        existing = db.query(Order).filter(
            Order.customer_contact == order.customer_contact,
            Order.product_details == order.product_details
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Duplicate order detected")
        
        # Create new order
        db_order = Order(**order.dict(), payment_status="pending", workflow_status=WorkflowStatus.received)
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
        return db_order
    finally:
        db.close()

@router.get("/", response_model=List[OrderResponse])
async def get_orders(status: Optional[str] = None):
    db = SessionLocal()
    try:
        query = db.query(Order)
        if status:
            query = query.filter(Order.workflow_status == status)
        return query.all()
    finally:
        db.close()

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    finally:
        db.close()