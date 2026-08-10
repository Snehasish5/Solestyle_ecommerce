from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models.user import AddressModel


class OrderItem(BaseModel):
    product_id: str
    name: str
    brand: str
    image: str
    price: float
    size: str
    color: str
    quantity: int
    subtotal: float


class CreateRazorpayOrder(BaseModel):
    address: AddressModel


class VerifyPayment(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    address: AddressModel


class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: List[OrderItem]
    address: AddressModel
    subtotal: float
    discount: float = 0.0
    total: float
    status: str  # pending, confirmed, shipped, delivered, cancelled
    payment_status: str  # paid, pending, failed
    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
