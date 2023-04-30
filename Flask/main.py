import os.path

from flask import Flask, request
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint

from Flask.models import db, User
from Flask.src.config import DB_HOST, DB_NAME, DB_PASS, DB_USER, DB_PORT

# app.config[
#     "SQLALCHEMY_DATABASE_URI"
# ] = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# swagger specific
SWAGGER_URL = "/swagger"
API_URL = os.path.normpath("/static/swagger.json")
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "MicroBlogging"}
)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prod.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

    api = Api(app)
    db.init_app(app)

    class TweetsApi(Resource):
        def get(self):
            """
            GET /api/tweets
            HTTP-Params:
            api-key: str
            """
            response = {
                "result": False,
                "error_type": str,
                "error_message": str,
            }
            if True:
                response = {
                    "result": True,
                    "tweets": [
                        {
                            "id": int,
                            "content": str,
                            "attachments": [],
                            "author": {
                                "id": int,
                                "name": str,
                            },
                            "likes": [
                                {
                                    "user_id": int,
                                    "name": str,
                                }
                            ],
                        },
                    ],
                }
            return response, 200

        def post(self):
            """
            POST /api/tweets
            HTTP-Params:
            api-key: str
            {
                “tweet_data”: string
                “tweet_media_ids”: Array[int]
            }
            """
            response = {"result": True, "tweet_id": int}
            return response, 200

        def delete(self, id: int):
            """
            DELETE /api/tweets/<id>
            HTTP-Params:
            api-key: str
            В ответ должно вернуться сообщение о статусе операции.
            {
                “result”: true
            }
            """
            response = {"result": False}
            if id:
                response = {"result": True}
            return response, 200

    class TweetsLikesApi(Resource):
        def post(self, id: int):
            """
            POST /api/tweets/<id>/likes
            HTTP-Params:
            api-key: str
            В ответ должно вернуться сообщение о статусе операции.
            {
            “result”: true
            }
            """
            response = {"result": False}
            if id:
                response = {"result": True}
            return response, 201

        def delete(self, id: int):
            """
            DELETE /api/tweets/<id>/likes
            HTTP-Params:
            api-key: str
            В ответ должно вернуться сообщение о статусе операции.
            {
                “result”: true
            }
            """
            response = {"result": False}
            if id:
                response = {"result": True}
            return response, 200

    class MediaApi(Resource):
        def post(self):
            """
            POST /api/medias
            HTTP-Params:
            api-key: str
            form: file=”image.jpg”
            В ответ должен вернуться id загруженного файла.
            {
                “result”: true,
                “media_id”: int
            }
            """
            response = {"result": True, "tweet_id": 1}
            return response, 201

    class UserApi(Resource):
        def get_me(self):
            """
            GET /api/users/me
            HTTP-Params:
            api-key: str
            """
            data = User.get_me()
            print(data)
            response = {
                "result": "true",
                "user": {
                    "id": data.id,
                    "name": data.name,
                    "followers": [{"id": "int", "name": "str"}],
                    "following": [{"id": "int", "name": "str"}],
                },
            }
            return response

        def get(self, id: int):
            """
            GET /api/users/<id>

            """
            response = {
                "result": "true",
                "user": {
                    "id": id,
                    "name": "str",
                    "followers": [{"id": "int", "name": "str"}],
                    "following": [{"id": "int", "name": "str"}],
                },
            }
            return response, 200

        def post(self, id: int):
            """
            POST /api/users/<id>/follow
            HTTP-Params:
            api-key: str
            В ответ должно вернуться сообщение о статусе операции.
            {
                “result”: true
            }
            """
            response = {"result": False}
            if id:
                response = {"result": True}
            return response, 201

        def delete(self, id: int):
            """DELETE /api/users/<id>/follow
            HTTP-Params:
            api-key: str
            В ответ должно вернуться сообщение о статусе операции.
            {
                “result”: true
            }
            """
            response = {"result": False}
            if id:
                response = {"result": True}
            return response, 200

        def dispatch_request(self, *args, **kwargs):
            # GET /api/users/me
            path = "/api/users/me"
            if path == request.path and request.method == "GET":
                self.get_me()
            else:
                return super().dispatch_request(*args, **kwargs)

            # # GET /api/users/<id>
            # elif request.method == 'GET':
            #     print(f'{request.path}')
            #     self.get(id=kwargs['id'])
            #
            # # POST /api/users/<id>/follow
            # elif request.method == 'POST' and 'follow' in request.path:
            #     print(f'{request.path}')
            #     self.post(id=kwargs['id'])
            #
            # # DELETE /api/users/<id>/follow
            # elif request.method == 'DELETE' and 'follow' in request.path:
            #     print(f'{request.path}')
            #     self.delete(id=kwargs['id'])

    # @app.route("/api/users/me", methods=["GET"])
    # def user_get_me():
    #     """
    #     GET /api/users/me
    #     HTTP-Params:
    #     api-key: str
    #     """
    #     data = User.get_me()
    #     print(data)
    #     response = {
    #         "result": "true",
    #         "user": {
    #             "id": data.id,
    #             "name": data.name,
    #             "followers": [{"id": "int", "name": "str"}],
    #             "following": [{"id": "int", "name": "str"}],
    #         },
    #     }
    #     return response

    api.add_resource(
        TweetsApi,
        "/api/tweets",
        "/api/tweets/<int:id>",
    )
    api.add_resource(
        TweetsLikesApi,
        "/api/tweets/<int:id>/likes",
    )

    api.add_resource(
        MediaApi,
        "/api/medias",
    )
    api.add_resource(
        UserApi,
        "/api/users/me",
        "/api/users/<int:id>",
        "/api/users/<int:id>/follow",
    )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
