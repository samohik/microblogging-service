from Flask.models import Follow


def test_app_config(app):
    assert not app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///test.db"


class TestTweetsApi:
    def test_get(self, client, db):
        response = client.get('/api/tweets')
        result = {
            'result': True,
            'tweets': [
                {
                    'attachments': [],
                    'author': {'id': 1, 'name': 'str'},  # TODO Tweet test_get author
                    'content': 'Test',
                    'id': 1,
                    'likes': [
                        {'name': 'V', 'user_id': 2},
                        {'name': 'Jade', 'user_id': 4}
                    ]
                }
            ]
        }
        assert response.status_code == 200
        assert response.json == result

    def test_post(self, client, db):
        response = client.post('/api/tweets', json={
            "tweet_data": "Test"
        })
        result = {'result': True, 'tweet_id': 3}
        assert response.status_code == 201
        assert response.json == result

    def test_delete(self, client, db):
        response = client.delete("/api/tweets/1")
        assert response.status_code == 204
        response = client.delete("/api/tweets/3")
        assert response.status_code == 400

    def test_post_likes(self, client):
        response = client.post("/api/tweets/1/likes")
        result = {"result": True}
        assert response.status_code == 201
        assert response.json == result

    def test_delete_likes(self, client):
        response = client.delete("/api/tweets/1/likes")
        assert response.status_code == 400
        response = client.delete("/api/tweets/2/likes")
        assert response.status_code == 204


class TestMediaApi:
    def test_post(self, client):
        # TODO media post
        response = client.post("/api/medias")
        result = {"result": True, "tweet_id": 1}
        assert response.status_code == 201
        assert response.json == result


class TestUserApi:
    def test_get_id(self, client):
        response = client.get("/api/users/2")
        result = {
            "result": True,
            "user": {
                "id": 2,
                "name": "V",
                "followers": [{"id": 1, "name": "Jonny"}],
                "following": [{'id': 4, 'name': 'Jade'}],
            },
        }
        assert response.status_code == 200
        assert response.json == result

    def test_get_me(self, client, db):
        response = client.get("/api/users/me")
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
        assert response.json == result

    def test_post_follow(self, client, db):
        response = client.post("/api/users/4/follow")
        follower_exist = Follow.get_follow(from_user=1, to_user=4)
        assert follower_exist == {'from': 1, 'to': 4}
        assert response.status_code == 201
        assert response.json == {'result': True}

    def test_delete_follow(self, client, db):
        response = client.delete("/api/users/2/follow")
        follower_exist = Follow.get_follow(from_user=1, to_user=2)
        assert follower_exist == {}
        assert response.status_code == 204
