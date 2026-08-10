from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    brand: str
    description: str
    price: float = Field(..., gt=0)
    original_price: Optional[float] = None
    category: str  # men, women, kids, unisex
    sub_category: Optional[str] = None  # running, casual, formal, sports
    images: List[str] = []  # list of image URLs
    sizes: List[str] = []   # ["6", "7", "8", "9", "10", "11"]
    colors: List[str] = []  # ["Black", "White", "Red"]
    stock: int = Field(default=0, ge=0)
    is_featured: bool = False
    is_new_arrival: bool = False
    tags: List[str] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    images: Optional[List[str]] = None
    sizes: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    stock: Optional[int] = None
    is_featured: Optional[bool] = None
    is_new_arrival: Optional[bool] = None
    tags: Optional[List[str]] = None


class ProductResponse(BaseModel):
    id: str
    name: str
    brand: str
    description: str
    price: float
    original_price: Optional[float] = None
    category: str
    sub_category: Optional[str] = None
    images: List[str]
    sizes: List[str]
    colors: List[str]
    stock: int
    is_featured: bool
    is_new_arrival: bool
    tags: List[str]
    average_rating: float = 0.0
    review_count: int = 0
    created_at: datetime


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=5, max_length=500)


class ReviewResponse(BaseModel):
    id: str
    user_id: str
    user_name: str
    rating: int
    comment: str
    created_at: datetime
