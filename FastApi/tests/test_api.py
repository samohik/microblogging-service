import json

import pytest
from fastapi import HTTPException

from auth.models import User
from models import Follow
from routers.tweet import get_tweets, post_tweets, delete_tweets, post_likes, delete_likes
from routers.user import get_user_id, post_follow, delete_follow
from schemas.tweet import TweetPost


class TestTweetsApi:
    async def test_get(self, async_db):
        user = await async_db.get(User, 1)

        response = await get_tweets(
            session=async_db,
            current_user=user,
        )
        result = {
            "result": True,
            "tweets": [
                {
                    "attachments": [],
                    "author": {"id": 1, "name": "str"},
                    "content": "Test",
                    "id": 1,
                    "likes": [
                        {"name": "V", "user_id": 2},
                        {"name": "Jade", "user_id": 4},
                    ],
                }
            ],
        }
        assert response.status_code == 200
        assert json.loads(response.body.decode('utf-8')) == result

    async def test_post(self, async_db):
        user = await async_db.get(User, 1)

        item = TweetPost(tweet_data="Test")

        response = await post_tweets(
            session=async_db,
            current_user=user,
            item=item,
        )
        result = {"result": True, "tweet_id": 3}
        assert response.status_code == 201
        assert json.loads(response.body.decode('utf-8')) == result

    async def test_delete(self, async_db):
        user = await async_db.get(User, 1)

        response = await delete_tweets(
            id=1,
            session=async_db,
            current_user=user,
        )
        assert response.status_code == 204

        with pytest.raises(HTTPException) as exc_info:
            await delete_tweets(
                id=3,
                session=async_db,
                current_user=user,
            )
        assert exc_info.value.status_code == 400

    async def test_post_likes(self, async_db):
        user = await async_db.get(User, 1)

        response = await post_likes(
            id=1,
            session=async_db,
            current_user=user,
        )
        result = {"result": True}
        assert response.status_code == 201
        assert json.loads(response.body.decode('utf-8')) == result

    async def test_delete_likes(self, async_db):
        user = await async_db.get(User, 1)

        with pytest.raises(HTTPException) as exc_info:
            await delete_likes(
                id=1,
                session=async_db,
                current_user=user,
            )
        assert exc_info.value.status_code == 400

        response = await delete_likes(
            id=2,
            session=async_db,
            current_user=user,
        )
        assert response.status_code == 204

# class TestMediaApi:
#     def test_post(self, client, async_db):
#         # TODO media post
#         response = client.post("/api/medias")
#         result = {"result": True, "tweet_id": 1}
#         assert response.status_code == 201
#         assert response.json == result


class TestUserApi:
    async def test_get_id(self, async_db):
        user = await async_db.get(User, 1)

        response = await get_user_id(
            id=2,
            session=async_db,
            current_user=user,
        )
        result = {
            "result": True,
            "user": {
                "id": 2,
                "name": "V",
                "followers": [{"id": 1, "name": "Jonny"}],
                "following": [{"id": 4, "name": "Jade"}],
            },
        }
        assert response.status_code == 200
        assert json.loads(response.body.decode('utf-8')) == result

    async def test_get_me(self, async_db):
        user = await async_db.get(User, 1)

        response = await get_user_id(
            id='me',
            session=async_db,
            current_user=user,
        )
        result = {
            "result": True,
            "user": {
                "id": 1,
                "name": "Jonny",
                "followers": [{"id": 3, "name": "Alt"}],
                "following": [{"id": 2, "name": "V"}],
            },
        }
        assert response.status_code == 200
        assert json.loads(response.body.decode('utf-8')) == result

    async def test_post_follow(self, client, async_db):
        user = await async_db.get(User, 1)

        response = await post_follow(
            id=4,
            session=async_db,
            current_user=user,
        )
        follower_exist = await Follow.get_follow(
            from_user=1,
            to_user=4,
            session=async_db,
        )
        assert follower_exist == {"from": 1, "to": 4}
        assert response.status_code == 201
        assert json.loads(response.body.decode('utf-8')) == {"result": True}

    async def test_delete_follow(self, client, async_db):
        user = await async_db.get(User, 1)

        response = await delete_follow(
            id=2,
            session=async_db,
            current_user=user,
        )
        follower_exist = await Follow.get_follow(
            from_user=1,
            to_user=2,
            session=async_db,
        )
        assert follower_exist == {}
        assert response.status_code == 204
        assert json.loads(response.body.decode('utf-8')) == {'result': True}
