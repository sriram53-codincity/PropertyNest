import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.main import app
from app.database.connection import get_db, Base
from app.models.mongo_models import PropertyDetails
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from sqlalchemy.pool import NullPool

import os

# Test Database URLs
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", "postgresql+asyncpg://postgres:9715907196@localhost:5432/homelease_test")
if os.environ.get("PG_PASSWORD") == "password":
    TEST_DATABASE_URL = "postgresql+asyncpg://postgres:password@localhost:5432/homelease_test"

TEST_MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://mathimaran12345678_db_user:9715907196@cluster0.evomuvp.mongodb.net/?appName=Cluster0")

@pytest_asyncio.fixture
async def db():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
    TestingSessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS property_nest"))
        await conn.run_sync(Base.metadata.create_all)

    # Setup Mongo
    mongo_client = AsyncIOMotorClient(TEST_MONGO_URL)
    mongo_db = mongo_client.homelease_test
    await init_beanie(database=mongo_db, document_models=[PropertyDetails])

    async with TestingSessionLocal() as session:
        yield session

    await engine.dispose()

@pytest_asyncio.fixture
async def client(db: AsyncSession):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
