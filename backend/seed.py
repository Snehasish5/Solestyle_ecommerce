import asyncio
from datetime import datetime
from database import products_collection, users_collection
from utils.security import hash_password


SAMPLE_PRODUCTS = [
    {
        "name": "Air Max Pulse",
        "brand": "Nike",
        "description": "The Nike Air Max Pulse draws inspiration from the London music scene, bringing raw style to the streets. The leather upper is textured for a tactile feel, while a textile inner sleeve adds comfort.",
        "price": 8995,
        "original_price": 11995,
        "category": "men",
        "sub_category": "casual",
        "images": [
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["7", "8", "9", "10", "11"],
        "colors": ["White", "Black"],
        "stock": 45,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["running", "lifestyle", "air-max"],
        "reviews": [],
    },

    {
        "name": "Ultra Boost 22",
        "brand": "Adidas",
        "description": "Designed for runners who need maximum cushioning. BOOST midsole technology returns energy to your every step while a Primeknit upper wraps your foot in adaptive support.",
        "price": 12999,
        "original_price": 15999,
        "category": "men",
        "sub_category": "running",
        "images": [
            "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["6", "7", "8", "9", "10", "11", "12"],
        "colors": ["Core Black", "Cloud White", "Solar Red"],
        "stock": 30,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["running", "ultraboost", "performance"],
        "reviews": [],
    },

    {
        "name": "Chuck Taylor All Star",
        "brand": "Converse",
        "description": "The iconic Chuck Taylor All Star has been a style staple since 1917. With its signature canvas upper and rubber outsole, this timeless sneaker brings classic cool to any outfit.",
        "price": 3995,
        "original_price": 4995,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["Black", "White", "Red", "Navy"],
        "stock": 80,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["casual", "classic", "canvas"],
        "reviews": [],
    },

    {
        "name": "Classic Suede",
        "brand": "Puma",
        "description": "The Puma Suede has been a cultural icon since 1968. Originally designed as a performance basketball shoe, it became a streetwear legend. Premium suede upper with iconic Puma Formstrip.",
        "price": 5999,
        "original_price": 7499,
        "category": "men",
        "sub_category": "casual",
        "images": [
            "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1552346154-21d32810aba3?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["7", "8", "9", "10", "11"],
        "colors": ["Peacoat", "Black", "White"],
        "stock": 25,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["casual", "suede", "classic"],
        "reviews": [],
    },

    {
        "name": "Old Skool",
        "brand": "Vans",
        "description": "The Old Skool, Vans first skate shoe with the iconic side stripe, has a low-top lace-up silhouette with a sturdy canvas and suede upper, padded collar for support and flexibility at the ankle.",
        "price": 4995,
        "original_price": 5995,
        "category": "unisex",
        "sub_category": "sports",
        "images": [
            "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10"],
        "colors": ["Black/White", "Navy", "Red"],
        "stock": 50,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["skate", "casual", "classic"],
        "reviews": [],
    },

    {
        "name": "Gel-Nimbus 25",
        "brand": "ASICS",
        "description": "The GEL-NIMBUS 25 shoe is our most cushioned everyday trainer designed for long-distance running. Features FF BLAST PLUS ECO cushioning and GEL technology for a plush ride.",
        "price": 14999,
        "original_price": 17999,
        "category": "men",
        "sub_category": "running",
        "images": [
            "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Black", "White", "Electric Blue"],
        "stock": 20,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["running", "performance", "long-distance"],
        "reviews": [],
    },

    {
        "name": "Air Force 1 '07",
        "brand": "Nike",
        "description": "The radiance lives on in the Nike Air Force 1 '07, the basketball original that puts a fresh spin on what you know best: durably stitched overlays, clean finishes and the perfect amount of flash.",
        "price": 7495,
        "original_price": 8495,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["6", "7", "8", "9", "10", "11"],
        "colors": ["White", "Black", "University Red"],
        "stock": 60,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["lifestyle", "basketball", "classic"],
        "reviews": [],
    },

    {
        "name": "RS-X Bold",
        "brand": "Puma",
        "description": "Inspired by the late '80s running culture, the RS-X Bold features a bulky silhouette with bold layers of material build-up for a futuristic look. Lightweight RS foam cushioning for all-day comfort.",
        "price": 7499,
        "original_price": 9999,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://images.unsplash.com/photo-1552346154-21d32810aba3?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1608231387042-66d1773070a5?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["4", "5", "6", "7", "8"],
        "colors": ["Puma White", "Luminous Pink"],
        "stock": 35,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["lifestyle", "bold", "retro"],
        "reviews": [],
    },

    {
        "name": "Stan Smith",
        "brand": "Adidas",
        "description": "Created in 1973 as a tennis shoe, the Stan Smith is now one of the most popular sneakers in history. The clean perforated leather upper and three-stripe details create timeless style.",
        "price": 6999,
        "original_price": 8499,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://images.unsplash.com/photo-1582588678413-dbf45f4823e9?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["Cloud White/Green", "Cloud White/Navy", "Black"],
        "stock": 55,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["tennis", "classic", "leather"],
        "reviews": [],
    },

    {
        "name": "Sneaker 574",
        "brand": "New Balance",
        "description": "Originally designed as a trail running shoe in 1988, the 574 has become one of New Balance's most iconic silhouettes. ENCAP midsole technology provides superior support and long-lasting durability.",
        "price": 6995,
        "original_price": 8495,
        "category": "men",
        "sub_category": "casual",
        "images": [
            "https://images.unsplash.com/photo-1539185441755-769473a23570?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1584735935682-2f2b69dff9d2?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Forest Green", "Navy", "Maroon"],
        "stock": 40,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["lifestyle", "retro", "ENCAP"],
        "reviews": [],
    },

    {
        "name": "Women's Free Run 5.0",
        "brand": "Nike",
        "description": "The Nike Free Run 5.0 gives you the flexibility to run with a barefoot feel. The flexible sole mimics your foot's natural movement with deep flex grooves, and the breathable upper keeps you cool.",
        "price": 5995,
        "original_price": 7495,
        "category": "women",
        "sub_category": "running",
        "images": [
            "https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["Photon Dust", "Black"],
        "stock": 28,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["running", "women", "flexible"],
        "reviews": [],
    },

    {
        "name": "Kids' Air Max 90",
        "brand": "Nike",
        "description": "Inspired by the original that debuted in 1990, the Nike Air Max 90 stays true to its OG running roots with the iconic Waffle outsole, stitched overlays and classic Max Air cushioning.",
        "price": 5495,
        "original_price": 6495,
        "category": "kids",
        "sub_category": "casual",
        "images": [
            "https://images.unsplash.com/photo-1514989940723-e8e51635b782?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?auto=format&fit=crop&w=800&q=80"
        ],
        "sizes": ["1", "2", "3", "4", "5"],
        "colors": ["White", "Black/White"],
        "stock": 20,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["kids", "casual", "air-max"],
        "reviews": [],
    },
]


async def seed_database():
    print("🌱 Starting database seed...")

    # Clear existing data
    await products_collection.delete_many({})
    print("🗑️  Cleared existing products")

    # Add timestamps
    for product in SAMPLE_PRODUCTS:
        product["created_at"] = datetime.utcnow()
        product["updated_at"] = datetime.utcnow()

    result = await products_collection.insert_many(SAMPLE_PRODUCTS)
    print(f"✅ Inserted {len(result.inserted_ids)} products")

    # Create a demo user if not exists
    existing = await users_collection.find_one({"email": "demo@solestyle.com"})

    if not existing:
        await users_collection.insert_one({
            "name": "Demo User",
            "email": "demo@solestyle.com",
            "phone": "9876543210",
            "password": hash_password("demo1234"),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        })

        print("✅ Demo user created: demo@solestyle.com / demo1234")

    print("🎉 Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_database())