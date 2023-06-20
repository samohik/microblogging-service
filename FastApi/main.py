from fastapi import FastAPI
from marshmallow import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from Flask.models import User, Follow, Tweet, Like
from Flask.schemas import TweetSchema
from database import Base, engine, get_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
#
#
# class TweetsApi:
#     @app.get('/api/tweets')
#     async def get(self, db: AsyncSession = get_db()):
#         """
#         GET /api/tweets
#         HTTP-Params:
#         api-key: str
#         """
#         user_id = 1
#         tweets = Tweet.get_tweets(user_id=user_id)
#
#         response = {
#             "result": True,
#             "tweets": [],
#         }
#         if tweets:
#             for tweet in tweets:
#                 likes = Like.get_likes(tweet_id=tweet.id)
#                 response["tweets"].append(
#                     {
#                         "id": tweet.id,
#                         "content": tweet.content,
#                         "attachments": [],
#                         "author": {
#                             "id": 1,
#                             "name": 'str',
#                         },
#                         "likes": [
#                             {"user_id": x.user_id, "name": x.user_backref.name} for x in likes
#                         ]
#                     }
#                 )
#         return response, 200
#
#     def post(self):
#         """
#         POST /api/tweets
#         HTTP-Params:
#         api-key: str
#         {
#             “tweet_data”: string
#             “tweet_media_ids”: Array[int]
#         }
#         """
#         data = request.json
#         schema = TweetSchema()
#         response = {
#             "result": False,
#             "error_type": str,
#             "error_message": str,
#         }
#         try:
#             validated_data = schema.load(data)
#         except ValidationError as e:
#             response["error_type"] = e
#             response["error_message"] = e.messages,
#             return response, 400
#
#         content = validated_data['tweet_data']
#         user_id = 1
#
#         tweet = Tweet.add_tweet(
#             user_id=user_id,
#             content=content,
#         )
#         if tweet:
#             # todo  add_media
#             # "tweet_media_ids": []
#             # Media.add_media(item) for item in tweet_media_ids
#
#             response = {
#                 "result": True,
#                 "tweet_id": tweet.id,
#             }
#             return response, 201
#         return response, 400
#
#     def delete(self, id: int):
#         """
#         DELETE /api/tweets/<id>
#         HTTP-Params:
#         api-key: str
#         В ответ должно вернуться сообщение о статусе операции.
#         {
#             “result”: true
#         }
#         """
#         user_id = 1
#         tweet = Tweet.delete(
#             user_id=user_id,
#             tweet_id=id,
#         )
#         response = {
#             "result": False,
#             #     "error_type": e,
#             #     "error_message": e.messages,
#         }
#         if tweet:
#             response = {"result": True}
#             return response, 204
#         return response, 400
#
#     def post_likes(self, id: int):
#         """
#         POST /api/tweets/<id>/likes
#         HTTP-Params:
#         api-key: str
#         В ответ должно вернуться сообщение о статусе операции.
#         {
#         “result”: true
#         }
#         """
#         user_id = 1
#         like = Like.add_like(
#             user_id=user_id,
#             tweet_id=id,
#         )
#         response = {
#             "result": False,
#             # todo error message
#             # "error_type": e,
#             # "error_message": e.messages,
#         }
#         if like:
#             response = {"result": True}
#         return response, 201
#
#     def delete_likes(self, id: int):
#         """
#         DELETE /api/tweets/<id>/likes
#         HTTP-Params:
#         api-key: str
#         В ответ должно вернуться сообщение о статусе операции.
#         {
#             “result”: true
#         }
#         """
#         user_id = 1
#         like = Like.delete(
#             user_id=user_id,
#             tweet_id=id,
#         )
#         response = {
#             "result": False,
#             # todo error message
#             # "error_type": e,
#             # "error_message": e.messages,
#         }
#         if like:
#             response = {"result": True}
#             return response, 204
#         return response, 400
#
#     def dispatch_request(self, *args, **kwargs):
#         # POST /api/tweets/<id>/likes
#         if "likes" in request.path and request.method == "POST":
#             return self.post_likes(kwargs["id"])
#
#         # DELETE /api/tweets/<id>/likes
#         elif "likes" in request.path and request.method == "DELETE":
#             return self.delete_likes(kwargs["id"])
#         else:
#             return super().dispatch_request(*args, **kwargs)
#
# class MediaApi(Resource):
#
#     def post(self):
#         """
#         POST /api/medias
#         HTTP-Params:
#         api-key: str
#         form: file=”image.jpg”
#         В ответ должен вернуться id загруженного файла.
#         {
#             “result”: true,
#             “media_id”: int
#         }
#         """
#         # todo post add_media
#         response = {"result": True, "tweet_id": 1}
#         return response, 201
#
# class UserApi(Resource):
#     def get(self, id: int):
#         """
#         GET /api/users/<id>
#         Пользователь может получить информацию о произвольном
#          профиле по его id:
#         """
#         user_exist = User.get_user(id)
#
#         follower = Follow.get_follower(id)
#         following = Follow.get_following(id)
#
#         if user_exist:
#             response = {
#                 "result": True,
#                 "user": user_exist
#             }
#             response["user"].update({"followers": follower})
#             response["user"].update({"following": following})
#         else:
#             response = {
#                 "result": False,
#                 #     "error_type": e,
#                 #     "error_message": e.messages,
#             }
#             return response, 400
#         return response, 200
#
#     def get_me(self, ):
#         """
#         GET /api/users/me
#         HTTP-Params:
#         api-key: str
#         """
#         self_id = 1
#         data = User.get_user(self_id)
#
#         follower = Follow.get_follower(self_id)
#         following = Follow.get_following(self_id)
#
#         response = {
#             "result": True,
#             "user": data
#         }
#         response["user"].update({"followers": follower})
#         response["user"].update({"following": following})
#         return response, 200
#
#     def post(self, id: int):
#         """
#         POST /api/users/<id>/follow
#         HTTP-Params:
#         api-key: str
#         В ответ должно вернуться сообщение о статусе операции.
#         {
#             “result”: true
#         }
#         """
#         result = Follow.handler_follower(
#             from_user_id=1,
#             to_user_id=id,
#             method="POST"
#         )
#         response = {
#             "result": False,
#             #     "error_type": e,
#             #     "error_message": e.messages,
#         }
#         if result:
#             response = {"result": True}
#         return response, 201
#
#     def delete(self, id: int):
#         """DELETE /api/users/<id>/follow
#         HTTP-Params:
#         api-key: str
#         В ответ должно вернуться сообщение о статусе операции.
#         {
#             “result”: true
#         }
#         """
#         result = Follow.handler_follower(
#             from_user_id=1,
#             to_user_id=id,
#             method="DELETE",
#         )
#         response = {
#             "result": False,
#             #     "error_type": e,
#             #     "error_message": e.messages,
#         }
#         if result:
#             response = {"result": True}
#         return response, 204
#
#     def dispatch_request(self, *args, **kwargs):
#         # GET /api/users/me
#         path = "/api/users/me"
#         if request.method == "GET" and request.path == path:
#             return self.get_me()
#         else:
#             return super().dispatch_request(*args, **kwargs)
#
# api.add_resource(
#     TweetsApi,
#     "/api/tweets",
#     "/api/tweets/<int:id>",
#     "/api/tweets/<int:id>/likes",
# )
#
# api.add_resource(
#     MediaApi,
#     "/api/medias",
# )
# api.add_resource(
#     UserApi,
#     "/api/users/me",
#     "/api/users/<int:id>",
#     "/api/users/<int:id>/follow",
# )

# return app


if __name__ == "__main__":
    # app.run(debug=True, host="0.0.0.0", port=5000)
    ...
