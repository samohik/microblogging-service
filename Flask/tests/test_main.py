def test_app_config(app):
    assert not app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///test.db"


# class TestTweetsApi:
#     def test_get(self, client):
#         response = client.get('/api/tweets')
#         result = {"result": True,
#                   "tweets": [
#                       {"id": id, "content": str, "attachments": [],
#                        "author": {"id": int, "name": str, },
#                        "likes": [{"user_id": int, "name": str, }], }, ], }
#         assert response.status_code == 200
#         assert response is True


class TestTweetsLikesApi:
    """Done"""

    def test_post(self, client):
        response = client.post("/api/tweets/1/likes")
        result = {"result": True}
        assert response.status_code == 201
        assert response.json == result

    def test_delete(self, client):
        response = client.delete("/api/tweets/1/likes")
        result = {"result": True}
        assert response.status_code == 200
        assert response.json == result


class TestMediaApi:
    """Done"""

    def test_post(self, client):
        response = client.post("/api/medias")
        result = {"result": True, "tweet_id": 1}

        assert response.status_code == 201
        assert response.json == result


class TestUserApi:
    def test_get_id(self, client):
        response = client.get("/api/users/1")
        result = {
            "result": "true",
            "user": {
                "id": 1,
                "name": "str",
                "followers": [{"id": "int", "name": "str"}],
                "following": [{"id": "int", "name": "str"}],
            },
        }
        assert response.status_code == 200
        assert response.json == result

    def test_get_me(self, client):
        response = client.get("/api/users/me")
        result = {
            "result": "true",
            "user": {
                "id": 1,
                "name": "Jonny",
                "followers": [{"id": 3, "name": "Alt"}],
                "following": [{"id": 2, "name": "V"}],
            },
        }
        assert response.status_code == 200
        assert response.json == result  # TODO (1, 'Jonny', None, None)

    def test_post(self, client):
        response = client.post("/api/users/1/follow", data=dict())
        assert response.status_code == 201

    def test_delete(self, client):
        response = client.delete("/api/users/1/follow")
        assert response.status_code == 200
