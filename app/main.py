import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Import all routes
from app.routes import (
    auth_routes,
    seller_request_routes,
    property_routes,
    application_routes,
    lease_routes,
    maintenance_routes,
    appointment_routes
)

from contextlib import asynccontextmanager
from beanie import init_beanie
from sqlalchemy import text
from app.database.connection import mongo_db, engine, Base
from app.models.mongo_models import PropertyDetails

# Import PG models so Base knows about them before creating tables
import app.models.pg_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the custom schema before tables
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS property_nest"))
        conn.commit()
    
    # Initialize PostgreSQL Tables
    Base.metadata.create_all(bind=engine)
    
    # Initialize Beanie with our Motor database and document models
    await init_beanie(database=mongo_db, document_models=[PropertyDetails])
    yield

# ── Create the FastAPI app ───────────────────────────────────
app = FastAPI(
    title="HomeLease Pro API",
    description="Property rental management platform — Register, list properties, apply for rent, manage leases and maintenance.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── Allow cross-origin requests (for frontend) ───────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # In production, replace * with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Serve uploaded files as static files ─────────────────────
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# ── Register all routes ──────────────────────────────────────
app.include_router(auth_routes.router)
app.include_router(seller_request_routes.router)
app.include_router(property_routes.router)
app.include_router(application_routes.router)
app.include_router(lease_routes.router)
app.include_router(maintenance_routes.router)
app.include_router(appointment_routes.router)


# ── Health check ─────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {"message": "HomeLease Pro API is running!", "docs": "/docs"}
