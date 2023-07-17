from models import Tweet, Follow


class TestTweetsApi:
    async def test_get(self, client, async_db):
        result = await Tweet.get_tweet(
            tweet_id=1,
            session=async_db,
        )
        assert result.id == 1
        response = await client.get("/api/tweets")
        result = {
            "result": True,
            "tweets": [
                {
                    "attachments": [],
                    "author": {"id": 1, "name": "str"},  # TODO Tweet test_get author
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
        assert response.json() == result

    async def test_post(self, client, async_db):
        response = await client.post(
            "/api/tweets",
            json={
                "tweet_data": "Test",
                # "tweet_media_ids": [1, 2],
            },
        )
        result = {"result": True, "tweet_id": 3}
        assert response.status_code == 201
        assert response.json() == result

    async def test_delete(self, client, async_db):
        response = await client.delete("/api/tweets/1")
        assert response.status_code == 204
        response = await client.delete("/api/tweets/3")
        assert response.status_code == 400

    async def test_post_likes(self, client, async_db):
        response = await client.post("/api/tweets/1/likes")
        result = {"result": True}
        assert response.status_code == 201
        assert response.json() == result

    async def test_delete_likes(self, client, async_db):
        response = await client.delete("/api/tweets/1/likes")
        assert response.status_code == 400
        response = await client.delete("/api/tweets/2/likes")
        assert response.status_code == 204


# class TestMediaApi:
#     def test_post(self, client, async_db):
#         # TODO media post
#         response = client.post("/api/medias")
#         result = {"result": True, "tweet_id": 1}
#         assert response.status_code == 201
#         assert response.json == result


class TestUserApi:
    async def test_get_id(self, client, async_db):
        response = await client.get("/api/users/2")
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
        assert response.json() == result

    async def test_get_me(self, client, async_db):
        response = await client.get("/api/users/me")
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
        assert response.json() == result

    async def test_post_follow(self, client, async_db):
        response = await client.post("/api/users/4/follow")
        follower_exist = await Follow.get_follow(
            from_user=1,
            to_user=4,
            session=async_db,
        )
        assert follower_exist == {"from": 1, "to": 4}
        assert response.status_code == 201
        assert response.json() == {"result": True}

    async def test_delete_follow(self, client, async_db):
        response = await client.delete("/api/users/2/follow")
        follower_exist = await Follow.get_follow(
            from_user=1,
            to_user=2,
            session=async_db,
        )
        assert follower_exist == {}
        assert response.status_code == 204
