from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from database import carts_collection, products_collection
from models.cart import CartItem, CartItemUpdate, CartResponse, CartItemResponse
from utils.security import get_current_user

router = APIRouter(prefix="/api/cart", tags=["Cart"])


async def get_cart_doc(user_id: str):
    cart = await carts_collection.find_one({"user_id": user_id})
    if not cart:
        cart = {"user_id": user_id, "items": []}
        await carts_collection.insert_one(cart)
    return cart


async def build_cart_response(cart: dict) -> CartResponse:
    items = []
    for item in cart.get("items", []):
        product = await products_collection.find_one({"_id": ObjectId(item["product_id"])})
        if product:
            subtotal = product["price"] * item["quantity"]
            items.append(CartItemResponse(
                product_id=item["product_id"],
                name=product["name"],
                brand=product["brand"],
                image=product["images"][0] if product.get("images") else "",
                price=product["price"],
                size=item["size"],
                color=item["color"],
                quantity=item["quantity"],
                subtotal=subtotal,
            ))
    total_items = sum(i.quantity for i in items)
    subtotal = sum(i.subtotal for i in items)
    return CartResponse(
        items=items,
        total_items=total_items,
        subtotal=subtotal,
        total=subtotal,
    )


@router.get("/", response_model=CartResponse)
async def get_cart(current_user: dict = Depends(get_current_user)):
    cart = await get_cart_doc(current_user["_id"])
    return await build_cart_response(cart)


@router.post("/add")
async def add_to_cart(item: CartItem, current_user: dict = Depends(get_current_user)):
    if not ObjectId.is_valid(item.product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")

    product = await products_collection.find_one({"_id": ObjectId(item.product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if item.size not in product.get("sizes", []):
        raise HTTPException(status_code=400, detail=f"Size {item.size} not available")
    if item.quantity > product.get("stock", 0):
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cart = await get_cart_doc(current_user["_id"])
    items = cart.get("items", [])

    # Check if same product+size+color already in cart
    existing_idx = next(
        (i for i, x in enumerate(items)
         if x["product_id"] == item.product_id and x["size"] == item.size and x["color"] == item.color),
        None
    )

    if existing_idx is not None:
        items[existing_idx]["quantity"] += item.quantity
    else:
        items.append(item.model_dump())

    await carts_collection.update_one(
        {"user_id": current_user["_id"]},
        {"$set": {"items": items}},
        upsert=True,
    )
    return {"message": "Item added to cart"}


@router.put("/item/{product_id}")
async def update_cart_item(product_id: str, size: str, color: str, data: CartItemUpdate, current_user: dict = Depends(get_current_user)):
    if data.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")

    cart = await get_cart_doc(current_user["_id"])
    items = cart.get("items", [])
    idx = next(
        (i for i, x in enumerate(items)
         if x["product_id"] == product_id and x["size"] == size and x["color"] == color),
        None
    )
    if idx is None:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    items[idx]["quantity"] = data.quantity
    await carts_collection.update_one({"user_id": current_user["_id"]}, {"$set": {"items": items}})
    return {"message": "Cart updated"}


@router.delete("/item/{product_id}")
async def remove_cart_item(product_id: str, size: str, color: str, current_user: dict = Depends(get_current_user)):
    cart = await get_cart_doc(current_user["_id"])
    items = [
        x for x in cart.get("items", [])
        if not (x["product_id"] == product_id and x["size"] == size and x["color"] == color)
    ]
    await carts_collection.update_one({"user_id": current_user["_id"]}, {"$set": {"items": items}})
    return {"message": "Item removed"}


@router.delete("/clear")
async def clear_cart(current_user: dict = Depends(get_current_user)):
    await carts_collection.update_one({"user_id": current_user["_id"]}, {"$set": {"items": []}})
    return {"message": "Cart cleared"}
