from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import MetaData


# DATABASE_URL = (
#     f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# )
DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
metadata = MetaData()
Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
