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

# Test Database URLs
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:9715907196@localhost:5432/homelease_test"
TEST_MONGO_URL = "mongodb+srv://mathimaran12345678_db_user:9715907196@cluster0.evomuvp.mongodb.net/?appName=Cluster0"

engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS property_nest"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    # Setup Mongo
    client = AsyncIOMotorClient(TEST_MONGO_URL)
    db = client.homelease_test
    await init_beanie(database=db, document_models=[PropertyDetails])

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await client.drop_database('homelease_test')

@pytest_asyncio.fixture
async def db():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(db: AsyncSession):
    async def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
