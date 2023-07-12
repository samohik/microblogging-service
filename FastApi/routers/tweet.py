from fastapi import Depends, APIRouter, Request
from marshmallow import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from database import get_async_session
from models import Tweet, Like
from schemas import TweetSchema

router = APIRouter()


@router.get('/api/tweets')
async def get_tweets(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    """
    GET /api/tweets
    HTTP-Params:
    api-key: str
    """
    self_id = request.headers.get('api-key')
    if not self_id:
        self_id = 1

    tweets = await Tweet.get_tweets(
        user_id=self_id,
        session=session,
    )

    response = {
        "result": True,
        "tweets": [],
    }
    if tweets:
        for tweet in tweets:
            likes = await Like.get_likes(
                tweet_id=tweet.id,
                session=session,
            )
            response["tweets"].append(
                {
                    "id": tweet.id,
                    "content": tweet.content,
                    "attachments": [],
                    "author": {
                        "id": 1,
                        "name": 'str',
                    },
                    "likes": [
                        {"user_id": x.user_id, "name": x.user_backref.name} for x in likes
                    ]
                }
            )
    return JSONResponse(response, status_code=200)


@router.post('/api/tweets')
async def post_tweets(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    """
    POST /api/tweets
    HTTP-Params:
    api-key: str
    {
        “tweet_data”: string
        “tweet_media_ids”: Array[int]
    }
    """

    self_id = request.headers.get('api-key')
    if not self_id:
        self_id = 1

    data = await request.json()
    schema = TweetSchema()

    response = {
        "result": False,
        "error_type": str,
        "error_message": str,
    }
    try:
        validated_data = schema.load(data)
    except ValidationError as e:
        response["error_type"] = e
        response["error_message"] = e.messages,

        return JSONResponse(response, status_code=400)

    content = validated_data['tweet_data']

    tweet = await Tweet.add_tweet(
        user_id=self_id,
        content=content,
        session=session,
    )
    if tweet:
        # todo  add_media
        # "tweet_media_ids": []
        # Media.add_media(item) for item in tweet_media_ids

        response = {
            "result": True,
            "tweet_id": tweet.id,
        }
        return JSONResponse(response, status_code=201)
    return JSONResponse(response, status_code=400)


@router.delete('/api/tweets/{id}')
async def delete_tweets(
        id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    """
    DELETE /api/tweets/<id>
    HTTP-Params:
    api-key: str
    В ответ должно вернуться сообщение о статусе операции.
    {
        “result”: true
    }
    """
    self_id = request.headers.get('api-key')
    if not self_id:
        self_id = 1

    tweet = await Tweet.delete(
        user_id=self_id,
        tweet_id=id,
        session=session
    )
    response = {
        "result": False,
        #     "error_type": e,
        #     "error_message": e.messages,
    }
    if tweet:
        response = {"result": True}
        return JSONResponse(response, status_code=204)

    return JSONResponse(response, status_code=400)


@router.post('/api/tweets/{id}/likes')
async def post_likes(
        id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    """
    POST /api/tweets/<id>/likes
    HTTP-Params:
    api-key: str
    В ответ должно вернуться сообщение о статусе операции.
    {
    “result”: true
    }
    """
    self_id = request.headers.get('api-key')
    if not self_id:
        self_id = 1
    like = await Like.add_like(
        user_id=self_id,
        tweet_id=id,
        session=session,
    )
    response = {
        "result": False,
        # todo error message
        # "error_type": e,
        # "error_message": e.messages,
    }
    if like:
        response = {"result": True}
    return JSONResponse(response, status_code=201)


@router.delete('/api/tweets/{id}/likes')
async def delete_likes(
        id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """
    DELETE /api/tweets/<id>/likes
    HTTP-Params:
    api-key: str
    В ответ должно вернуться сообщение о статусе операции.
    {
        “result”: true
    }
    """
    user_id = 1
    like = await Like.delete(
        user_id=user_id,
        tweet_id=id,
        session=session
    )
    response = {
        "result": False,
        # todo error message
        # "error_type": e,
        # "error_message": e.messages,
    }
    if like:
        response = {"result": True}
        return JSONResponse(response, status_code=204)
    return JSONResponse(response, status_code=400)
