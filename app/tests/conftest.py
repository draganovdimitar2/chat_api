import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel
from app import app
from app.db.main import get_session
from app.config import Config

DB_URL = Config.TEST_DATABASE_URL
engine = create_async_engine(DB_URL, echo=True)
TestingSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# session override
async def override_get_session() -> AsyncSession:
    async with TestingSessionLocal() as session:
        yield session


# 3) build a single async_client fixture
@pytest.fixture(scope="session")
async def async_client():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # override the dependency
    app.dependency_overrides[get_session] = override_get_session

    # using ASGITransport so no real network is used
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
