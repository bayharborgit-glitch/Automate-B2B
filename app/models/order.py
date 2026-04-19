from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship  # ← CRITICAL IMPORT
from datetime import datetime
from enum import Enum as PyEnum
from app.database import Base

class PaymentStatus(PyEnum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"

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
    customer_name = Column(String, nullable=False)
    customer_contact = Column(String, nullable=False)
    product_details = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.pending)
    workflow_status = Column(Enum(WorkflowStatus), default=WorkflowStatus.received)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ← ADD THIS RELATIONSHIP (you already added this part)
    refunds = relationship("Refund", back_populates="order", cascade="all, delete-orphan")