from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.config import settings
from backend.database import create_indexes
from backend.routes import auth, products, cart, wishlist, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()

    print(f"{settings.app_name} API is running!")

    yield

    print("Shutting down...")


app = FastAPI(
    title=f"{settings.app_name} API",
    description="E-commerce API for SoleStyle shoe store",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "null"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    auth.router,
    prefix="/api"
)

app.include_router(
    products.router,
    prefix="/api"
)

app.include_router(
    cart.router,
    prefix="/api"
)

app.include_router(
    wishlist.router,
    prefix="/api"
)

app.include_router(
    orders.router,
    prefix="/api"
)


@app.get("/api")
async def root():
    return {
        "message": f"Welcome to {settings.app_name} API",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name
    }