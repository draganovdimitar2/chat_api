from sqlmodel import SQLModel
from app.config import Config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

engine = create_async_engine(url=Config.DATABASE_URL)
