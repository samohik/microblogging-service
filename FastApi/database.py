from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# DATABASE_URL = (
#     f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# )
DATABASE_URL = "sqlite+aiosqlite:///./app.db"

Base = declarative_base()
metadata = MetaData()

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
