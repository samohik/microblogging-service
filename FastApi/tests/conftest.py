import asyncio
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from FastApi.models import Base, User, Tweet, Follow
from database import metadata
from main import app

TEST_DATABASE = "sqlite+aiosqlite:///./test_app.db"

engine_test = create_async_engine(TEST_DATABASE, poolclass=NullPool)
test_async_session = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session() as session:
        yield session


# app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="function")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all())
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all())


@pytest.fixture(scope="function")
async def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest.fixture(scope="function")
async def async_db(prepare_database, event_loop):
    async with test_async_session() as session:
        yield session



# async def x():
#     async with async_session() as session:
#         # Users
#         user_me = User(name="Jonny")
#         user_id_2 = User(
#             name="V",
#         )
#         user_id_3 = User(
#             name="Alt",
#         )
#         user_id_4 = User(
#             name="Jade",
#         )
#         session.add(user_me)
#         session.add(user_id_2)
#         session.add(user_id_3)
#         session.add(user_id_4)
#         session.flush()
#
#         # Subscribers
#         follower_me = Follow(
#             to_user_id=user_me.id,
#             from_user_id=user_id_3.id,
#         )
#
#         # Am signed to
#         following_me = Follow(
#             to_user_id=user_id_2.id,
#             from_user_id=user_me.id,
#         )
#         following_2 = Follow(
#             to_user_id=user_id_4.id,
#             from_user_id=user_id_2.id,
#         )
#
#         # Tweet
#         tweet_me = Tweet(
#             content='Test',
#             user_id=user_me.id,
#         )
#         tweet_user_2 = Tweet(
#             content='Test2',
#             user_id=user_id_2.id,
#         )
#
#         session.add(follower_me)
#         session.add(following_me)
#         session.add(following_2)
#         session.add(tweet_me)
#         session.add(tweet_user_2)
#         session.flush()
#
#         # Like
#         like_to_user_2 = Like(
#             user_id=user_me.id,
#             tweet_id=tweet_user_2.id,
#         )
#         like_from_user_2 = Like(
#             user_id=user_id_2.id,
#             tweet_id=tweet_me.id,
#         )
#         like_from_user_4 = Like(
#             user_id=user_id_4.id,
#             tweet_id=tweet_me.id,
#         )
