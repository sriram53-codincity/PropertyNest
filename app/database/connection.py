import os
import urllib.parse
from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from motor.motor_asyncio import AsyncIOMotorClient

PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = urllib.parse.quote_plus(os.getenv("PG_PASSWORD", "password"))
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", 5432)
PG_DATABASE = os.getenv("PG_DATABASE", "homelease")

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

metadata = MetaData(schema="property_nest")
Base = declarative_base(metadata=metadata)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB  = os.getenv("MONGO_DB", "homelease")

mongo_client = AsyncIOMotorClient(MONGO_URL)
mongo_db = mongo_client[MONGO_DB]
