import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from FastApi.models import *


TEST_DATABASE = "sqlite+aiosqlite:///./test_app.db"


@pytest.fixture(scope="session")
def engine():
    engine_test = create_async_engine(TEST_DATABASE, poolclass=NullPool)
    Base.metadata.create_all(engine_test)

    yield engine

    Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def async_db(engine):
    test_async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    yield test_async_session


@pytest.fixture(scope="function")
async def db(async_db):
    async with async_db() as session:
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
