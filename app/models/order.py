from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from app.database import Base

class WorkflowStatus(PyEnum):
    received = "received"
    processing = "processing"
    notified = "notified"
    paused = "paused"
    manual_review = "manual_review"
    completed = "completed"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    customer_contact = Column(String)
    product_details = Column(String)
    quantity = Column(Integer, default=1)
    total_price = Column(Float)
    payment_method = Column(String)
    payment_status = Column(String, default="pending")
    workflow_status = Column(Enum(WorkflowStatus), default=WorkflowStatus.received)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())