from pydantic import BaseModel
from typing import List, Optional


class CartItem(BaseModel):
    product_id: str
    size: str
    color: str
    quantity: int = 1


class CartItemUpdate(BaseModel):
    quantity: int


class CartItemResponse(BaseModel):
    product_id: str
    name: str
    brand: str
    image: str
    price: float
    size: str
    color: str
    quantity: int
    subtotal: float


class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_items: int
    subtotal: float
    discount: float = 0.0
    total: float
