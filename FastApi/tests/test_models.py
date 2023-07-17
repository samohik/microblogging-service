import pytest
from sqlalchemy import select

from auth.models import User
from models import (
    Follow,
    Tweet,
    Like,
)


async def test_db(async_db):
    user = User(
        name='Test',
        email='678@gmail.com',
        hashed_password='4567'
    )
    async_db.add(user)
    await async_db.commit()
    res1 = await async_db.get(User, 1)
    assert res1.name == 'Jonny'

    query = await async_db.execute(select(User).where(User.name == 'Test'))
    res2 = query.scalar_one()
    assert res2.name == 'Test'


class TestUser:
    async def test_get_user(self, async_db):
        data_2 = await User.get_user(
            id=2,
            session=async_db,
        )
        data_wrong = await User.get_user(
            id=8,
            session=async_db,
        )
        assert data_2 == {'id': 2, 'name': 'V'}
        assert data_wrong == {}


class TestFollow:
    async def test_get_follower_exist(self, async_db):
        result = await Follow.get_follow(
            session=async_db,
            from_user=1,
            to_user=2
        )
        assert result == {'from': 1, 'to': 2}

    async def test_get_follower_dont_exist(self, async_db):
        result = await Follow.get_follow(
            session=async_db,
            from_user=1,
            to_user=4
        )
        assert result == {}

    async def test_get_follower(self, async_db):
        data = await Follow.get_follower(
            session=async_db,
            id=1
        )
        assert data == [{'id': 3, 'name': 'Alt'}]

    async def test_get_following(self, async_db):
        data = await Follow.get_following(
            session=async_db,
            id=1
        )
        assert data == [{'id': 2, 'name': 'V'}]

    async def test_add_follower(self, async_db):
        data = await Follow.handler_follower(
            session=async_db,
            to_user_id=4,
            from_user_id=1,
            method="POST",
        )
        result = await Follow.get_follow(
            session=async_db,
            from_user=1,
            to_user=4,
        )
        assert data is True
        assert result == {"to": 4, "from": 1}

    async def test_delete_follower(self, async_db):
        result = await Follow.get_follow(
            session=async_db,
            from_user=1,
            to_user=2
        )
        data = await Follow.handler_follower(
            session=async_db,
            to_user_id=2,
            from_user_id=1,
            method="DELETE",
        )
        assert result == {"to": 2, "from": 1}
        assert data is True


class TestTweet:
    async def test_get(self, async_db):
        result = await Tweet.get_tweet(
            tweet_id=1,
            session=async_db,
        )
        assert result.id == 1

    async def test_add(self, async_db):
        content = 'Test'
        result = await Tweet.add_tweet(
            session=async_db,
            user_id=1,
            content=content,
        )
        assert result.id == 3

    async def test_delete(self, async_db):
        result = await Tweet.delete(
            user_id=1,
            tweet_id=1,
            session=async_db,
        )
        assert result is True
        result = await Tweet.delete(
            user_id=1,
            tweet_id=2,
            session=async_db,
        )
        assert result is False


class TestLike:
    async def test_get(self, async_db):

        data = await Like.get_likes(
            tweet_id=1,
            session=async_db,
        )
        result = [x.id for x in data]
        assert result == [2, 3, ]

    async def test_add(self, async_db):
        result1 = await Like.add_like(
            session=async_db,
            tweet_id=1,
            user_id=3,
        )
        assert result1 is True
        result2 = await Like.add_like(
            session=async_db,
            tweet_id=1,
            user_id=2,
        )
        assert result2 is False

    async def test_delete(self, async_db):
        result1 = await Like.delete(
            session=async_db,
            tweet_id=1,
            user_id=2,
        )
        assert result1 is True
        result2 = await Like.delete(
            session=async_db,
            tweet_id=1,
            user_id=3,
        )
        assert result2 is False
