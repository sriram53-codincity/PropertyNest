import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

# ── PostgreSQL Setup (SQLAlchemy) ──────────────────────────────
import urllib.parse
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = urllib.parse.quote_plus(os.getenv("PG_PASSWORD", "password"))
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", 5432)
PG_DATABASE = os.getenv("PG_DATABASE", "homelease")

SQLALCHEMY_DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
from sqlalchemy import MetaData

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData(schema="property_nest")
Base = declarative_base(metadata=metadata)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── MongoDB Setup (Beanie / Motor) ─────────────────────────────
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB  = os.getenv("MONGO_DB", "homelease")

# We create the motor client, but Beanie initialization 
# requires an async context, which we will do in main.py
mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo_db = mongo_client[MONGO_DB]
