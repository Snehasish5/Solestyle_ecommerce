from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime
from database import wishlists_collection, products_collection
from utils.security import get_current_user

router = APIRouter(prefix="/api/wishlist", tags=["Wishlist"])


async def get_wishlist_doc(user_id: str):
    wishlist = await wishlists_collection.find_one({"user_id": user_id})
    if not wishlist:
        wishlist = {"user_id": user_id, "product_ids": []}
        await wishlists_collection.insert_one(wishlist)
    return wishlist


@router.get("/")
async def get_wishlist(current_user: dict = Depends(get_current_user)):
    wishlist = await get_wishlist_doc(current_user["_id"])
    product_ids = wishlist.get("product_ids", [])

    products = []
    for pid in product_ids:
        if ObjectId.is_valid(pid):
            p = await products_collection.find_one({"_id": ObjectId(pid)})
            if p:
                reviews = p.get("reviews", [])
                avg = round(sum(r["rating"] for r in reviews) / len(reviews), 1) if reviews else 0
                products.append({
                    "id": str(p["_id"]),
                    "name": p["name"],
                    "brand": p["brand"],
                    "price": p["price"],
                    "original_price": p.get("original_price"),
                    "image": p["images"][0] if p.get("images") else "",
                    "sizes": p.get("sizes", []),
                    "average_rating": avg,
                    "review_count": len(reviews),
                    "stock": p.get("stock", 0),
                })
    return {"products": products, "count": len(products)}


@router.post("/add/{product_id}")
async def add_to_wishlist(product_id: str, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = await products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    wishlist = await get_wishlist_doc(current_user["_id"])
    if product_id in wishlist.get("product_ids", []):
        return {"message": "Already in wishlist"}

    await wishlists_collection.update_one(
        {"user_id": current_user["_id"]},
        {"$push": {"product_ids": product_id}},
        upsert=True,
    )
    return {"message": "Added to wishlist"}


@router.delete("/remove/{product_id}")
async def remove_from_wishlist(product_id: str, current_user: dict = Depends(get_current_user)):
    await wishlists_collection.update_one(
        {"user_id": current_user["_id"]},
        {"$pull": {"product_ids": product_id}}
    )
    return {"message": "Removed from wishlist"}


@router.get("/check/{product_id}")
async def check_wishlist(product_id: str, current_user: dict = Depends(get_current_user)):
    wishlist = await get_wishlist_doc(current_user["_id"])
    return {"in_wishlist": product_id in wishlist.get("product_ids", [])}
