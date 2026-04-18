from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrderBase(BaseModel):
    customer_name: str
    customer_contact: str
    product_details: str
    quantity: int = 1
    total_price: float
    payment_method: str

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    payment_status: str
    workflow_status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True