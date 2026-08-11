from fastapi import APIRouter, HTTPException, Query, Depends, status
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from database import products_collection
from models.product import ProductCreate, ProductUpdate, ProductResponse, ReviewCreate
from utils.security import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


def serialize_product(p: dict) -> dict:
    reviews = p.get("reviews", [])
    avg_rating = round(sum(r["rating"] for r in reviews) / len(reviews), 1) if reviews else 0.0
    return {
        "id": str(p["_id"]),
        "name": p["name"],
        "brand": p["brand"],
        "description": p["description"],
        "price": p["price"],
        "original_price": p.get("original_price"),
        "category": p["category"],
        "sub_category": p.get("sub_category"),
        "images": p.get("images", []),
        "sizes": p.get("sizes", []),
        "colors": p.get("colors", []),
        "stock": p.get("stock", 0),
        "is_featured": p.get("is_featured", False),
        "is_new_arrival": p.get("is_new_arrival", False),
        "tags": p.get("tags", []),
        "average_rating": avg_rating,
        "review_count": len(reviews),
        "created_at": p["created_at"],
    }


@router.get("/", response_model=dict)
async def list_products(
    search: Optional[str] = None,
    category: Optional[str] = None,
    brand: Optional[str] = None,
    sub_category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    size: Optional[str] = None,
    color: Optional[str] = None,
    is_featured: Optional[bool] = None,
    is_new_arrival: Optional[bool] = None,
    sort_by: Optional[str] = "created_at",  # price_asc, price_desc, rating, newest
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=12, le=50),
):
    query = {}

    if search:
        query["$text"] = {"$search": search}
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    if brand:
        query["brand"] = {"$regex": brand, "$options": "i"}
    if sub_category:
        query["sub_category"] = {"$regex": sub_category, "$options": "i"}
    if min_price is not None or max_price is not None:
        query["price"] = {}
        if min_price is not None:
            query["price"]["$gte"] = min_price
        if max_price is not None:
            query["price"]["$lte"] = max_price
    if size:
        query["sizes"] = size
    if color:
        query["colors"] = {"$regex": color, "$options": "i"}
    if is_featured is not None:
        query["is_featured"] = is_featured
    if is_new_arrival is not None:
        query["is_new_arrival"] = is_new_arrival

    sort_map = {
        "price_asc": [("price", 1)],
        "price_desc": [("price", -1)],
        "newest": [("created_at", -1)],
        "rating": [("average_rating", -1)],
    }
    sort_order = sort_map.get(sort_by, [("created_at", -1)])

    total = await products_collection.count_documents(query)
    skip = (page - 1) * limit

    cursor = products_collection.find(query).sort(sort_order).skip(skip).limit(limit)
    products = [serialize_product(p) async for p in cursor]

    return {
        "products": products,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
    }


@router.get("/featured", response_model=List[dict])
async def get_featured():
    cursor = products_collection.find({"is_featured": True}).limit(8)
    return [serialize_product(p) async for p in cursor]


@router.get("/new-arrivals", response_model=List[dict])
async def get_new_arrivals():
    cursor = products_collection.find({"is_new_arrival": True}).sort("created_at", -1).limit(8)
    return [serialize_product(p) async for p in cursor]


@router.get("/{product_id}", response_model=dict)
async def get_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return serialize_product(product)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate, current_user: dict = Depends(get_current_user)):
    product_doc = data.model_dump()
    product_doc["created_at"] = datetime.utcnow()
    product_doc["reviews"] = []
    result = await products_collection.insert_one(product_doc)
    product_doc["_id"] = result.inserted_id
    return serialize_product(product_doc)


@router.put("/{product_id}")
async def update_product(product_id: str, data: ProductUpdate, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    update_data["updated_at"] = datetime.utcnow()
    result = await products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product updated"}


@router.delete("/{product_id}")
async def delete_product(product_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    result = await products_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}


@router.post("/{product_id}/reviews")
async def add_review(product_id: str, data: ReviewCreate, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    review = {
        "id": str(ObjectId()),
        "user_id": current_user["_id"],
        "user_name": current_user["name"],
        "rating": data.rating,
        "comment": data.comment,
        "created_at": datetime.utcnow(),
    }
    result = await products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$push": {"reviews": review}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Review added", "review": review}


@router.get("/{product_id}/reviews")
async def get_reviews(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    product = await products_collection.find_one({"_id": ObjectId(product_id)}, {"reviews": 1})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product.get("reviews", [])
