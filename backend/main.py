from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from database import create_indexes
from routes import auth, products, cart, wishlist, orders

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_indexes()
    print(f"{settings.app_name} API is running!")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(
    title=f"{settings.app_name} API",
    description="E-commerce API for SoleStyle shoe store",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url,"https://solestyle-ecommerce-two.vercel.app", "http://localhost:5500", "http://127.0.0.1:5500", "https://solestylee.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name} API", "docs": "/docs"}


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": settings.app_name}
