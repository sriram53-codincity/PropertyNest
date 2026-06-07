import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

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

import app.models.pg_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS property_nest"))
        await conn.run_sync(Base.metadata.create_all)
    
    await init_beanie(database=mongo_db, document_models=[PropertyDetails])
    yield

app = FastAPI(
    title="HomeLease Pro API",
    description="Property rental management platform — Register, list properties, apply for rent, manage leases and maintenance.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.include_router(auth_routes.router)
app.include_router(seller_request_routes.router)
app.include_router(property_routes.router)
app.include_router(application_routes.router)
app.include_router(lease_routes.router)
app.include_router(maintenance_routes.router)
app.include_router(appointment_routes.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "HomeLease Pro API is running!", "docs": "/docs"}
