import asyncio
import os
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from models import User, Follow, Tweet, Like
from database import Base, metadata, get_async_session
from main import app


# test_db_file = os.path.abspath('')
test_db_file = os.path.dirname(__file__)
# "FastApi", "tests", "test_app.db"
print(test_db_file)
TEST_DATABASE = f"sqlite+aiosqlite:///{test_db_file}/test_app.db"

engine_test = create_async_engine(TEST_DATABASE, poolclass=NullPool)
test_async_session = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


@pytest.fixture(scope="function")
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_db():
    async with test_async_session() as session:
        await preloaded_data(session)
        yield session


client = TestClient(app)


@pytest.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


async def preloaded_data(session: AsyncSession):
    # Users
    user_me = User(name="Jonny")
    user_id_2 = User(
        name="V",
    )
    user_id_3 = User(
        name="Alt",
    )
    user_id_4 = User(
        name="Jade",
    )
    session.add(user_me)
    session.add(user_id_2)
    session.add(user_id_3)
    session.add(user_id_4)
    await session.flush()

    # Subscribers
    follower_me = Follow(
        to_user_id=user_me.id,
        from_user_id=user_id_3.id,
    )

    # Am signed to
    following_me = Follow(
        to_user_id=user_id_2.id,
        from_user_id=user_me.id,
    )
    following_2 = Follow(
        to_user_id=user_id_4.id,
        from_user_id=user_id_2.id,
    )

    # Tweet
    tweet_me = Tweet(
        content='Test',
        user_id=user_me.id,
    )
    tweet_user_2 = Tweet(
        content='Test2',
        user_id=user_id_2.id,
    )

    session.add(follower_me)
    session.add(following_me)
    session.add(following_2)
    session.add(tweet_me)
    session.add(tweet_user_2)
    await session.flush()

    # Like
    like_to_user_2 = Like(
        user_id=user_me.id,
        tweet_id=tweet_user_2.id,
    )
    like_from_user_2 = Like(
        user_id=user_id_2.id,
        tweet_id=tweet_me.id,
    )
    like_from_user_4 = Like(
        user_id=user_id_4.id,
        tweet_id=tweet_me.id,
    )
    session.add(like_to_user_2)
    session.add(like_from_user_2)
    session.add(like_from_user_4)
    await session.commit()


