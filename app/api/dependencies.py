from sqlmodel import SQLModel
from app.config import Config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

"""Database setup"""
engine = create_async_engine(url=Config.DATABASE_URL)
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


"""Dependency"""


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
