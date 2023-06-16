import unittest

from FastApi.database import Base
from FastApi.models import User, Follow, Tweet, Like
from FastApi.tests.conftest import engine_test, async_session


class BaseTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        engine = engine_test
        self.session = async_session()

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

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
        async with self.session.begin():
            self.session.add(user_me)
            self.session.add(user_id_2)
            self.session.add(user_id_3)
            self.session.add(user_id_4)
            self.session.flush()

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
        async with self.session.begin():
            self.session.add(follower_me)
            self.session.add(following_me)
            self.session.add(following_2)
            self.session.add(tweet_me)
            self.session.add(tweet_user_2)
            self.session.flush()

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

    async def asyncTearDown(self):
        # Close the session and drop the tables
        await self.session.close()

        engine = self.session.get_bind()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


class TestUser(BaseTest):
    async def test_get_user(self):
        data_2 = await User.get_user(2)
        data_wrong = await User.get_user(8)

        assert data_2 == {'id': 2, 'name': 'V'}
        assert data_wrong == {}


class TestFollow:
    def test_get_follower_exist(self, db):
        result = Follow.get_follow(from_user=1, to_user=2)
        assert result == {'from': 1, 'to': 2}

    def test_get_follower_dont_exist(self, db):
        result = Follow.get_follow(from_user=1, to_user=4)
        assert result == {}

    def test_get_follower(self, db):
        data = Follow.get_follower()
        assert data == [{'id': 3, 'name': 'Alt'}]

    def test_get_following(self, db):
        data = Follow.get_following()
        assert data == [{'id': 2, 'name': 'V'}]

    def test_add_follower(self, db):
        data = Follow.handler_follower(
            to_user_id=4,
            from_user_id=1,
            method="POST",
        )
        result = Follow.get_follow(from_user=1, to_user=4)
        assert data is True
        assert result == {"to": 4, "from": 1}

    def test_delete_follower(self, db):
        result = Follow.get_follow(from_user=1, to_user=2)
        data = Follow.handler_follower(
            to_user_id=2,
            from_user_id=1,
            method="DELETE",
        )
        assert result == {"to": 2, "from": 1}
        assert data is True


class TestTweet:
    def test_get(self, db):
        result = Tweet.get_tweet(1)
        assert result.id == 1

    def test_add(self, db):
        content = 'Test'
        result = Tweet.add_tweet(1, content)
        assert result.id == 3

    def test_delete(self, db):
        result = Tweet.delete(
            user_id=1,
            tweet_id=1
        )
        assert result is True
        result = Tweet.delete(
            user_id=1,
            tweet_id=2
        )
        assert result is False


class TestLike:
    def test_get(self, db):
        data = Like.get_likes(1)
        result = [x.id for x in data]
        assert result == [2, 3, ]

    def test_add(self, db):
        result = Like.add_like(
            tweet_id=1,
            user_id=3,
        )
        assert result is True
        result = Like.add_like(
            tweet_id=1,
            user_id=2,
        )
        assert result is False

    def test_delete(self, db):
        result = Like.delete(
            tweet_id=1,
            user_id=2,
        )
        assert result is True
        result = Like.delete(
            tweet_id=1,
            user_id=3,
        )
        assert result is False


if __name__ == '__main__':
    unittest.main()
