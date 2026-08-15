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

    {
        "name": "Nike Dunk Low Retro",
        "brand": "Nike",
        "description": "The Nike Dunk Low Retro brings classic basketball-inspired style to everyday streetwear with a clean low-top silhouette and comfortable cushioning.",
        "price": 8495,
        "original_price": 9995,
        "category": "men",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/sneakers?lock=101",
            "https://loremflickr.com/800/800/sneakers?lock=102"
        ],
        "sizes": ["7", "8", "9", "10", "11"],
        "colors": ["White/Black", "University Blue"],
        "stock": 42,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["dunk", "casual", "streetwear"],
        "reviews": [],
    },

    {
        "name": "Jordan 1 Low",
        "brand": "Nike",
        "description": "The Air Jordan 1 Low delivers the iconic Jordan look in a sleek low-top design with classic color blocking and everyday comfort.",
        "price": 8995,
        "original_price": 10995,
        "category": "men",
        "sub_category": "sports",
        "images": [
            "https://loremflickr.com/800/800/sneakers?lock=103",
            "https://loremflickr.com/800/800/sneakers?lock=104"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Black/Red", "White/Black"],
        "stock": 32,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["jordan", "basketball", "lifestyle"],
        "reviews": [],
    },

    {
        "name": "Pegasus 40",
        "brand": "Nike",
        "description": "The Nike Pegasus 40 is an everyday running shoe designed with responsive cushioning, breathable materials and a smooth ride.",
        "price": 7995,
        "original_price": 9495,
        "category": "men",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/running-shoes?lock=105",
            "https://loremflickr.com/800/800/running-shoes?lock=106"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Black", "White", "Blue"],
        "stock": 38,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["running", "pegasus", "training"],
        "reviews": [],
    },

    {
        "name": "React Infinity Run",
        "brand": "Nike",
        "description": "Built for comfortable daily miles, the React Infinity Run combines responsive foam cushioning with a supportive upper for smooth running.",
        "price": 9995,
        "original_price": 11995,
        "category": "women",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/running-shoes?lock=107",
            "https://loremflickr.com/800/800/sport-shoes?lock=108"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["White/Pink", "Black/White"],
        "stock": 27,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["running", "react", "women"],
        "reviews": [],
    },

    {
        "name": "Air Max 270",
        "brand": "Nike",
        "description": "The Air Max 270 features a bold lifestyle design with a large visible Air unit and a lightweight upper designed for all-day comfort.",
        "price": 10995,
        "original_price": 12995,
        "category": "men",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/sneakers?lock=109",
            "https://loremflickr.com/800/800/sport-shoes?lock=110"
        ],
        "sizes": ["7", "8", "9", "10", "11"],
        "colors": ["Black/White", "Grey/Red"],
        "stock": 24,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["air-max", "lifestyle", "streetwear"],
        "reviews": [],
    },

    {
        "name": "Revolution 6",
        "brand": "Nike",
        "description": "The Nike Revolution 6 provides lightweight cushioning and a simple breathable design suitable for running, workouts and daily activities.",
        "price": 3995,
        "original_price": 4995,
        "category": "women",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/womens-shoes?lock=111",
            "https://loremflickr.com/800/800/running-shoes?lock=112"
        ],
        "sizes": ["4", "5", "6", "7", "8"],
        "colors": ["White", "Black", "Pink"],
        "stock": 46,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["running", "training", "women"],
        "reviews": [],
    },

    {
        "name": "Forum Low",
        "brand": "Adidas",
        "description": "The Adidas Forum Low combines vintage basketball aesthetics with a modern low-top silhouette and signature Adidas detailing.",
        "price": 6999,
        "original_price": 8499,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/sneakers?lock=113",
            "https://loremflickr.com/800/800/adidas-shoes?lock=114"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["White/Blue", "White/Black"],
        "stock": 36,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["forum", "basketball", "retro"],
        "reviews": [],
    },

    {
        "name": "Gazelle Indoor",
        "brand": "Adidas",
        "description": "The Gazelle Indoor brings classic terrace style with a premium suede upper, gum outsole and iconic Adidas three-stripe branding.",
        "price": 7999,
        "original_price": 9499,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/suede-shoes?lock=115",
            "https://loremflickr.com/800/800/casual-shoes?lock=116"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["Green/White", "Pink/White"],
        "stock": 29,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["gazelle", "retro", "casual"],
        "reviews": [],
    },

    {
        "name": "Adizero Boston 12",
        "brand": "Adidas",
        "description": "A performance running shoe designed for speed sessions and long-distance training with responsive cushioning and lightweight construction.",
        "price": 11999,
        "original_price": 13999,
        "category": "men",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/running-shoes?lock=117",
            "https://loremflickr.com/800/800/athletic-shoes?lock=118"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Solar Red", "Black/White"],
        "stock": 18,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["running", "adizero", "performance"],
        "reviews": [],
    },

    {
        "name": "Superstar",
        "brand": "Adidas",
        "description": "The Adidas Superstar is a timeless sneaker featuring the iconic shell toe, classic three stripes and a versatile low-top silhouette.",
        "price": 5999,
        "original_price": 7499,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/classic-sneakers?lock=119",
            "https://loremflickr.com/800/800/white-sneakers?lock=120"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["White/Black", "White/Red"],
        "stock": 61,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["superstar", "classic", "casual"],
        "reviews": [],
    },

    {
        "name": "NMD_R1",
        "brand": "Adidas",
        "description": "The NMD_R1 blends modern streetwear styling with responsive cushioning and a comfortable sock-like upper.",
        "price": 8999,
        "original_price": 10999,
        "category": "men",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/adidas-sneakers?lock=121",
            "https://loremflickr.com/800/800/modern-sneakers?lock=122"
        ],
        "sizes": ["7", "8", "9", "10", "11"],
        "colors": ["Core Black", "Cloud White"],
        "stock": 33,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["nmd", "streetwear", "lifestyle"],
        "reviews": [],
    },

    {
        "name": "Samba OG",
        "brand": "Adidas",
        "description": "The Samba OG combines its football-inspired heritage with a sleek low-profile design that has become a modern streetwear classic.",
        "price": 8999,
        "original_price": 9999,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/football-shoes?lock=123",
            "https://loremflickr.com/800/800/retro-sneakers?lock=124"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["Black/White", "White/Green"],
        "stock": 44,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["samba", "football", "streetwear"],
        "reviews": [],
    },

    {
        "name": "RS-X Efekt",
        "brand": "Puma",
        "description": "The RS-X Efekt features a chunky retro-inspired silhouette with layered materials and comfortable cushioning.",
        "price": 7999,
        "original_price": 9499,
        "category": "men",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/chunky-sneakers?lock=125",
            "https://loremflickr.com/800/800/puma-shoes?lock=126"
        ],
        "sizes": ["7", "8", "9", "10", "11"],
        "colors": ["White/Grey", "Black/Orange"],
        "stock": 31,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["rs-x", "retro", "lifestyle"],
        "reviews": [],
    },

    {
        "name": "Puma Rider FV",
        "brand": "Puma",
        "description": "The Puma Rider FV updates classic running-inspired styling with a lightweight construction and bold layered design.",
        "price": 6999,
        "original_price": 8499,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/puma-sneakers?lock=127",
            "https://loremflickr.com/800/800/womens-sneakers?lock=128"
        ],
        "sizes": ["4", "5", "6", "7", "8"],
        "colors": ["White/Pink", "Grey/Blue"],
        "stock": 26,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["rider", "retro", "women"],
        "reviews": [],
    },

    {
        "name": "Puma Velocity Nitro 2",
        "brand": "Puma",
        "description": "A lightweight running shoe featuring responsive cushioning designed to provide a smooth and energetic ride for daily training.",
        "price": 9999,
        "original_price": 11999,
        "category": "men",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/puma-running-shoes?lock=129",
            "https://loremflickr.com/800/800/performance-shoes?lock=130"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Black/Yellow", "Blue/White"],
        "stock": 22,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["running", "nitro", "performance"],
        "reviews": [],
    },

    {
        "name": "Suede Classic XXI",
        "brand": "Puma",
        "description": "The Suede Classic XXI preserves the iconic Puma silhouette with a soft suede upper and signature Formstrip branding.",
        "price": 5499,
        "original_price": 6999,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/suede-sneakers?lock=131",
            "https://loremflickr.com/800/800/puma-casual-shoes?lock=132"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["Black/White", "Pink/White"],
        "stock": 48,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["suede", "classic", "casual"],
        "reviews": [],
    },

    {
        "name": "Fresh Foam X 1080",
        "brand": "New Balance",
        "description": "The Fresh Foam X 1080 is designed for everyday runners seeking soft cushioning, a smooth ride and comfortable long-distance performance.",
        "price": 12995,
        "original_price": 14995,
        "category": "men",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/new-balance-running?lock=133",
            "https://loremflickr.com/800/800/running-shoes?lock=134"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Grey/Blue", "Black/White"],
        "stock": 19,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["running", "fresh-foam", "performance"],
        "reviews": [],
    },

    {
        "name": "New Balance 327",
        "brand": "New Balance",
        "description": "The New Balance 327 takes inspiration from classic 1970s running shoes and gives the silhouette a bold modern streetwear identity.",
        "price": 7995,
        "original_price": 9495,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/new-balance-sneakers?lock=135",
            "https://loremflickr.com/800/800/retro-running-shoes?lock=136"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["Cream/Green", "Grey/White"],
        "stock": 37,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["327", "retro", "lifestyle"],
        "reviews": [],
    },

    {
        "name": "New Balance 550",
        "brand": "New Balance",
        "description": "The 550 brings back a classic basketball silhouette with clean leather-inspired styling and a versatile low-top profile.",
        "price": 8995,
        "original_price": 10495,
        "category": "unisex",
        "sub_category": "sports",
        "images": [
            "https://loremflickr.com/800/800/basketball-sneakers?lock=137",
            "https://loremflickr.com/800/800/new-balance-550?lock=138"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["White/Green", "White/Blue"],
        "stock": 34,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["550", "basketball", "retro"],
        "reviews": [],
    },

    {
        "name": "New Balance 9060",
        "brand": "New Balance",
        "description": "The 9060 combines futuristic styling with classic New Balance design cues, offering a bold chunky silhouette for everyday wear.",
        "price": 11995,
        "original_price": 13995,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/futuristic-sneakers?lock=139",
            "https://loremflickr.com/800/800/chunky-shoes?lock=140"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["Sea Salt", "Grey/Pink"],
        "stock": 21,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["9060", "lifestyle", "chunky"],
        "reviews": [],
    },

    {
        "name": "Gel-Kayano 30",
        "brand": "ASICS",
        "description": "The GEL-KAYANO 30 is designed for supportive everyday running with advanced cushioning and a stable comfortable ride.",
        "price": 13999,
        "original_price": 15999,
        "category": "men",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/asics-running-shoes?lock=141",
            "https://loremflickr.com/800/800/stability-running-shoes?lock=142"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Black/Blue", "White/Red"],
        "stock": 17,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["kayano", "running", "stability"],
        "reviews": [],
    },

    {
        "name": "Novablast 4",
        "brand": "ASICS",
        "description": "The Novablast 4 is a lightweight daily trainer with energetic cushioning designed for runners who want a responsive ride.",
        "price": 11999,
        "original_price": 13999,
        "category": "women",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/asics-shoes?lock=143",
            "https://loremflickr.com/800/800/womens-running-shoes?lock=144"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["Pink/White", "Black/Purple"],
        "stock": 23,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["novablast", "running", "women"],
        "reviews": [],
    },

    {
        "name": "Gel-Lyte III",
        "brand": "ASICS",
        "description": "The GEL-LYTE III combines classic 1990s running heritage with modern lifestyle styling and signature split-tongue construction.",
        "price": 7999,
        "original_price": 9499,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/asics-sneakers?lock=145",
            "https://loremflickr.com/800/800/retro-shoes?lock=146"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["Cream/Green", "Black/Grey"],
        "stock": 39,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["gel-lyte", "retro", "lifestyle"],
        "reviews": [],
    },

    {
        "name": "Chuck 70 High Top",
        "brand": "Converse",
        "description": "The Chuck 70 High Top upgrades the iconic Converse design with premium canvas, enhanced cushioning and classic high-top styling.",
        "price": 4995,
        "original_price": 5995,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/converse-shoes?lock=147",
            "https://loremflickr.com/800/800/high-top-sneakers?lock=148"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["Black", "Parchment", "White"],
        "stock": 52,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["chuck-70", "high-top", "classic"],
        "reviews": [],
    },

    {
        "name": "Run Star Hike",
        "brand": "Converse",
        "description": "The Run Star Hike combines the classic Converse canvas upper with an exaggerated platform sole for a bold modern streetwear look.",
        "price": 6995,
        "original_price": 7995,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/platform-sneakers?lock=149",
            "https://loremflickr.com/800/800/womens-platform-shoes?lock=150"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["Black/White", "White/Black"],
        "stock": 28,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["platform", "streetwear", "women"],
        "reviews": [],
    },

    {
        "name": "Old Skool Platform",
        "brand": "Vans",
        "description": "The Old Skool Platform adds extra height to Vans' iconic skate-inspired silhouette while retaining the signature side stripe.",
        "price": 5999,
        "original_price": 6999,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/vans-shoes?lock=151",
            "https://loremflickr.com/800/800/platform-shoes?lock=152"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["Black/White", "White"],
        "stock": 41,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["vans", "platform", "skate"],
        "reviews": [],
    },

    {
        "name": "Sk8-Hi",
        "brand": "Vans",
        "description": "The Sk8-Hi is an iconic high-top skate shoe featuring the classic Vans side stripe, padded collar and durable construction.",
        "price": 6499,
        "original_price": 7499,
        "category": "men",
        "sub_category": "sports",
        "images": [
            "https://loremflickr.com/800/800/vans-skate-shoes?lock=153",
            "https://loremflickr.com/800/800/high-top-skate-shoes?lock=154"
        ],
        "sizes": ["7", "8", "9", "10", "11"],
        "colors": ["Black/White", "Navy/White"],
        "stock": 35,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["sk8-hi", "skate", "high-top"],
        "reviews": [],
    },

    {
        "name": "Bradley Mid",
        "brand": "Fila",
        "description": "The Fila Bradley Mid combines classic basketball-inspired styling with a comfortable high-top silhouette for casual everyday wear.",
        "price": 4499,
        "original_price": 5499,
        "category": "men",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/fila-shoes?lock=155",
            "https://loremflickr.com/800/800/basketball-shoes?lock=156"
        ],
        "sizes": ["7", "8", "9", "10", "11"],
        "colors": ["White/Navy", "White/Red"],
        "stock": 47,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["fila", "basketball", "casual"],
        "reviews": [],
    },

    {
        "name": "Disruptor II",
        "brand": "Fila",
        "description": "The Fila Disruptor II is a bold chunky sneaker with a distinctive platform sole and retro-inspired streetwear aesthetic.",
        "price": 5499,
        "original_price": 6499,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/fila-sneakers?lock=157",
            "https://loremflickr.com/800/800/chunky-platform-shoes?lock=158"
        ],
        "sizes": ["4", "5", "6", "7", "8"],
        "colors": ["White", "White/Pink"],
        "stock": 30,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["fila", "chunky", "platform"],
        "reviews": [],
    },

    {
        "name": "Bradley Lo",
        "brand": "Fila",
        "description": "A clean low-top sneaker inspired by classic court shoes, featuring a versatile design suitable for everyday casual outfits.",
        "price": 3999,
        "original_price": 4999,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/fila-court-shoes?lock=159",
            "https://loremflickr.com/800/800/low-top-sneakers?lock=160"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10"],
        "colors": ["White", "Black/White"],
        "stock": 56,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["fila", "court", "casual"],
        "reviews": [],
    },

    {
        "name": "Cloudswift 3",
        "brand": "On",
        "description": "The Cloudswift 3 is designed for urban running with responsive cushioning and a lightweight construction built for hard surfaces.",
        "price": 14999,
        "original_price": 16999,
        "category": "men",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/on-running-shoes?lock=161",
            "https://loremflickr.com/800/800/urban-running-shoes?lock=162"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Black", "White/Blue"],
        "stock": 16,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["on", "running", "urban"],
        "reviews": [],
    },

    {
        "name": "Cloud 5",
        "brand": "On",
        "description": "The Cloud 5 is a lightweight lifestyle and training shoe featuring a distinctive sole design and comfortable everyday cushioning.",
        "price": 12999,
        "original_price": 14999,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/on-cloud-shoes?lock=163",
            "https://loremflickr.com/800/800/womens-training-shoes?lock=164"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["White", "All Black"],
        "stock": 25,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["on", "lifestyle", "cloud"],
        "reviews": [],
    },

    {
        "name": "Court Vision Low",
        "brand": "Nike",
        "description": "The Nike Court Vision Low takes inspiration from classic basketball sneakers with a clean low-top design made for everyday street style.",
        "price": 4495,
        "original_price": 5495,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/nike-court-shoes?lock=165",
            "https://loremflickr.com/800/800/low-top-court-shoes?lock=166"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["White/Black", "White/Blue"],
        "stock": 63,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["court", "basketball", "casual"],
        "reviews": [],
    },

    {
        "name": "Blazer Mid '77",
        "brand": "Nike",
        "description": "The Nike Blazer Mid '77 combines vintage basketball styling with a classic high-top silhouette and bold oversized Swoosh branding.",
        "price": 8495,
        "original_price": 9995,
        "category": "women",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/nike-high-top-shoes?lock=167",
            "https://loremflickr.com/800/800/vintage-basketball-shoes?lock=168"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["White/Black", "White/Red"],
        "stock": 29,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["blazer", "basketball", "vintage"],
        "reviews": [],
    },

    {
        "name": "ZoomX Invincible Run",
        "brand": "Nike",
        "description": "The ZoomX Invincible Run is designed for comfortable daily mileage with highly responsive cushioning and a smooth energetic ride.",
        "price": 13995,
        "original_price": 15995,
        "category": "men",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/nike-running-shoes?lock=169",
            "https://loremflickr.com/800/800/performance-running-shoes?lock=170"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Black/White", "Blue/Green"],
        "stock": 14,
        "is_featured": True,
        "is_new_arrival": True,
        "tags": ["zoomx", "running", "performance"],
        "reviews": [],
    },

    {
        "name": "Adistar 2",
        "brand": "Adidas",
        "description": "The Adistar 2 is built for long-distance running with supportive cushioning and a comfortable design for extended training sessions.",
        "price": 9999,
        "original_price": 11999,
        "category": "men",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/adidas-running-shoes?lock=171",
            "https://loremflickr.com/800/800/long-distance-running-shoes?lock=172"
        ],
        "sizes": ["7", "8", "9", "10", "11", "12"],
        "colors": ["Black/White", "Grey/Blue"],
        "stock": 20,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["adistar", "running", "training"],
        "reviews": [],
    },

    {
        "name": "Cloudnova",
        "brand": "On",
        "description": "The Cloudnova blends athletic performance with modern lifestyle styling, making it suitable for workouts and everyday urban movement.",
        "price": 11999,
        "original_price": 13999,
        "category": "unisex",
        "sub_category": "sports",
        "images": [
            "https://loremflickr.com/800/800/on-sports-shoes?lock=173",
            "https://loremflickr.com/800/800/urban-sneakers?lock=174"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["White/Black", "Black/White"],
        "stock": 22,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["on", "training", "lifestyle"],
        "reviews": [],
    },

    {
        "name": "574 Core",
        "brand": "New Balance",
        "description": "The New Balance 574 Core is a versatile classic combining retro running inspiration with everyday comfort and durable construction.",
        "price": 6495,
        "original_price": 7995,
        "category": "unisex",
        "sub_category": "casual",
        "images": [
            "https://loremflickr.com/800/800/new-balance-574?lock=175",
            "https://loremflickr.com/800/800/retro-sneakers?lock=176"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["Grey", "Navy", "Black"],
        "stock": 58,
        "is_featured": True,
        "is_new_arrival": False,
        "tags": ["574", "classic", "retro"],
        "reviews": [],
    },

    {
        "name": "Gel-Contend 8",
        "brand": "ASICS",
        "description": "The GEL-CONTEND 8 offers reliable cushioning and support for casual runners and everyday fitness activities.",
        "price": 5999,
        "original_price": 6999,
        "category": "women",
        "sub_category": "running",
        "images": [
            "https://loremflickr.com/800/800/asics-running?lock=177",
            "https://loremflickr.com/800/800/womens-running?lock=178"
        ],
        "sizes": ["4", "5", "6", "7", "8", "9"],
        "colors": ["Black/Pink", "White/Blue"],
        "stock": 43,
        "is_featured": False,
        "is_new_arrival": False,
        "tags": ["asics", "running", "training"],
        "reviews": [],
    },

    {
        "name": "Era Classic",
        "brand": "Vans",
        "description": "The Vans Era is a classic low-top skate shoe featuring a durable canvas upper, padded collar and timeless casual styling.",
        "price": 4499,
        "original_price": 5499,
        "category": "unisex",
        "sub_category": "sports",
        "images": [
            "https://loremflickr.com/800/800/vans-era-shoes?lock=179",
            "https://loremflickr.com/800/800/skate-sneakers?lock=180"
        ],
        "sizes": ["5", "6", "7", "8", "9", "10", "11"],
        "colors": ["Black/White", "Red/White"],
        "stock": 49,
        "is_featured": False,
        "is_new_arrival": True,
        "tags": ["vans", "era", "skate"],
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