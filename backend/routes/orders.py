import hmac
import hashlib
import uuid
import razorpay
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime
from database import orders_collection, carts_collection, products_collection
from models.order import CreateRazorpayOrder, VerifyPayment, OrderResponse
from utils.security import get_current_user
from config import settings

router = APIRouter(prefix="/api/orders", tags=["Orders"])

razorpay_client = razorpay.Client(
    auth=(settings.razorpay_key_id, settings.razorpay_key_secret)
)


async def get_cart_items(user_id: str):
    """Fetch and build order items from user's cart."""
    cart = await carts_collection.find_one({"user_id": user_id})
    if not cart or not cart.get("items"):
        raise HTTPException(status_code=400, detail="Cart is empty")

    order_items = []
    total = 0

    for item in cart["items"]:
        product = await products_collection.find_one(
            {"_id": ObjectId(item["product_id"])}
        )

        if not product:
            continue

        subtotal = product["price"] * item["quantity"]
        total += subtotal

        order_items.append({
            "product_id": item["product_id"],
            "name": product["name"],
            "brand": product["brand"],
            "image": product["images"][0] if product.get("images") else "",
            "price": product["price"],
            "size": item["size"],
            "color": item["color"],
            "quantity": item["quantity"],
            "subtotal": subtotal,
        })

    return order_items, total


@router.post("/create-razorpay-order")
async def create_razorpay_order(
    data: CreateRazorpayOrder,
    current_user: dict = Depends(get_current_user)
):
    """Create a Razorpay order for the user's current cart."""

    order_items, total = await get_cart_items(current_user["_id"])

    if not order_items:
        raise HTTPException(
            status_code=400,
            detail="No valid items in cart"
        )

    amount_paise = int(total * 100)  # Razorpay uses paise

    # Razorpay receipt must be 40 characters or fewer
    receipt = f"rcpt_{uuid.uuid4().hex[:16]}"

    razorpay_order = razorpay_client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "receipt": receipt,
        "notes": {
            "user_id": current_user["_id"],
            "user_name": current_user["name"],
            "user_email": current_user["email"],
        }
    })

    return {
        "razorpay_order_id": razorpay_order["id"],
        "amount": amount_paise,
        "currency": "INR",
        "key": settings.razorpay_key_id,
        "items": order_items,
        "total": total,
        "user": {
            "name": current_user["name"],
            "email": current_user["email"],
            "phone": current_user.get("phone", ""),
        }
    }


@router.post("/verify-payment", status_code=201)
async def verify_payment(
    data: VerifyPayment,
    current_user: dict = Depends(get_current_user)
):
    """Verify Razorpay signature and create order in DB."""

    # HMAC-SHA256 signature verification
    expected_signature = hmac.new(
        key=settings.razorpay_key_secret.encode(),
        msg=f"{data.razorpay_order_id}|{data.razorpay_payment_id}".encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    if expected_signature != data.razorpay_signature:
        raise HTTPException(
            status_code=400,
            detail="Invalid payment signature"
        )

    order_items, total = await get_cart_items(current_user["_id"])

    order_doc = {
        "user_id": current_user["_id"],
        "items": order_items,
        "address": data.address.model_dump(),
        "subtotal": total,
        "discount": 0.0,
        "total": total,
        "status": "confirmed",
        "payment_status": "paid",
        "razorpay_order_id": data.razorpay_order_id,
        "razorpay_payment_id": data.razorpay_payment_id,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = await orders_collection.insert_one(order_doc)

    # Clear cart after successful order
    await carts_collection.update_one(
        {"user_id": current_user["_id"]},
        {"$set": {"items": []}}
    )

    # Update stock for each product
    for item in order_items:
        await products_collection.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": -item["quantity"]}}
        )

    return {
        "message": "Order placed successfully",
        "order_id": str(result.inserted_id)
    }


@router.get("/")
async def list_orders(
    current_user: dict = Depends(get_current_user)
):
    cursor = orders_collection.find(
        {"user_id": current_user["_id"]}
    ).sort("created_at", -1)

    orders = []

    async for order in cursor:
        orders.append({
            "id": str(order["_id"]),
            "items": order["items"],
            "total": order["total"],
            "status": order["status"],
            "payment_status": order["payment_status"],
            "created_at": order["created_at"],
            "item_count": len(order["items"]),
        })

    return {"orders": orders}


@router.get("/{order_id}")
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid order ID"
        )

    order = await orders_collection.find_one({
        "_id": ObjectId(order_id),
        "user_id": current_user["_id"]
    })

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return {
        "id": str(order["_id"]),
        "user_id": order["user_id"],
        "items": order["items"],
        "address": order["address"],
        "subtotal": order["subtotal"],
        "discount": order.get("discount", 0),
        "total": order["total"],
        "status": order["status"],
        "payment_status": order["payment_status"],
        "razorpay_order_id": order.get("razorpay_order_id"),
        "razorpay_payment_id": order.get("razorpay_payment_id"),
        "created_at": order["created_at"],
        "updated_at": order["updated_at"],
    }


@router.put("/{order_id}/cancel")
async def cancel_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid order ID"
        )

    order = await orders_collection.find_one({
        "_id": ObjectId(order_id),
        "user_id": current_user["_id"]
    })

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order["status"] not in ["confirmed", "pending"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel an order that is '{order['status']}'"
        )

    await orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {
                "status": "cancelled",
                "updated_at": datetime.utcnow()
            }
        }
    )

    # Restore stock
    for item in order["items"]:
        await products_collection.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": item["quantity"]}}
        )

    return {"message": "Order cancelled successfully"}