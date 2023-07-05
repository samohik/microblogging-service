import pytest
from sqlalchemy import select

from models import (
    User,
    Follow,
    Tweet,
    Like,
)


async def test_db(async_db):
    user = User(name='Test')
    async_db.add(user)
    await async_db.commit()
    query = (await async_db.execute(select(User).where(User.id == 1)))
    res = query.scalar_one()
    assert res.name == 'Jonny'
    # assert res.name == 'Test'


class TestUser:
    async def test_get_user(self, async_db):
        data_2 = await User.get_user(2)
        data_wrong = await User.get_user(8)

        assert data_2 == {'id': 2, 'name': 'V'}
        assert data_wrong == {}


# class TestFollow:
#     def test_get_follower_exist(self, db):
#         result = Follow.get_follow(from_user=1, to_user=2)
#         assert result == {'from': 1, 'to': 2}
#
#     def test_get_follower_dont_exist(self, db):
#         result = Follow.get_follow(from_user=1, to_user=4)
#         assert result == {}
#
#     def test_get_follower(self, db):
#         data = Follow.get_follower()
#         assert data == [{'id': 3, 'name': 'Alt'}]
#
#     def test_get_following(self, db):
#         data = Follow.get_following()
#         assert data == [{'id': 2, 'name': 'V'}]
#
#     def test_add_follower(self, db):
#         data = Follow.handler_follower(
#             to_user_id=4,
#             from_user_id=1,
#             method="POST",
#         )
#         result = Follow.get_follow(from_user=1, to_user=4)
#         assert data is True
#         assert result == {"to": 4, "from": 1}
#
#     def test_delete_follower(self, db):
#         result = Follow.get_follow(from_user=1, to_user=2)
#         data = Follow.handler_follower(
#             to_user_id=2,
#             from_user_id=1,
#             method="DELETE",
#         )
#         assert result == {"to": 2, "from": 1}
#         assert data is True
#
#
# class TestTweet:
#     def test_get(self, db):
#         result = Tweet.get_tweet(1)
#         assert result.id == 1
#
#     def test_add(self, db):
#         content = 'Test'
#         result = Tweet.add_tweet(1, content)
#         assert result.id == 3
#
#     def test_delete(self, db):
#         result = Tweet.delete(
#             user_id=1,
#             tweet_id=1
#         )
#         assert result is True
#         result = Tweet.delete(
#             user_id=1,
#             tweet_id=2
#         )
#         assert result is False
#
#
# class TestLike:
#     def test_get(self, db):
#         data = Like.get_likes(1)
#         result = [x.id for x in data]
#         assert result == [2, 3, ]
#
#     def test_add(self, db):
#         result = Like.add_like(
#             tweet_id=1,
#             user_id=3,
#         )
#         assert result is True
#         result = Like.add_like(
#             tweet_id=1,
#             user_id=2,
#         )
#         assert result is False
#
#     def test_delete(self, db):
#         result = Like.delete(
#             tweet_id=1,
#             user_id=2,
#         )
#         assert result is True
#         result = Like.delete(
#             tweet_id=1,
#             user_id=3,
#         )
#         assert result is False
