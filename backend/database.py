import motor.motor_asyncio
from config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
database = client.sole_ecommerce

# Collections
users_collection = database.get_collection("users")
products_collection = database.get_collection("products")
carts_collection = database.get_collection("carts")
wishlists_collection = database.get_collection("wishlists")
orders_collection = database.get_collection("orders")


async def create_indexes():
    """Create database indexes for performance."""
    await users_collection.create_index("email", unique=True)
    await products_collection.create_index("name")
    await products_collection.create_index("brand")
    await products_collection.create_index("category")
    await products_collection.create_index([("name", "text"), ("brand", "text"), ("description", "text")])
    await carts_collection.create_index("user_id")
    await wishlists_collection.create_index("user_id")
    await orders_collection.create_index("user_id")
    print("✅ Database indexes created")
