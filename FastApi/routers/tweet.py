
from fastapi import Depends, APIRouter, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from database import get_async_session
from models import Tweet, Like
from schemas.base import Success
from schemas.tweet import TweetGet, TweetPost, TweetPostSuccess

router = APIRouter()


@router.get(
    '/api/tweets', tags=['Tweet'],
    response_model=TweetGet
)
async def get_tweets(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Get all tweets created by you.
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
                        {
                            "user_id": x.user_id,
                            "name": x.user_backref.name
                        } for x in likes
                    ]
                }
            )
    return JSONResponse(response, status_code=200)


@router.post(
    '/api/tweets',
    tags=['Tweet'],
    response_model=TweetPostSuccess,
)
async def post_tweets(
        item: TweetPost,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Create new tweet.
    """
    self_id = request.headers.get('api-key')
    if not self_id:
        self_id = 1

    if item.dict():
        content = item.tweet_data

        tweet = await Tweet.add_tweet(
            user_id=self_id,
            content=content,
            session=session,
        )
        if tweet:
            # add_media
            # "tweet_media_ids": []
            # Media.add_media(item) for item in tweet_media_ids

            response = {
                "result": True,
                "tweet_id": tweet.id,
            }
            return JSONResponse(response, status_code=201)
    raise HTTPException(
        status_code=400,
        detail="Data not valid."
    )


@router.delete(
    '/api/tweets/{id}',
    tags=['Tweet'],
    response_model=Success
)
async def delete_tweets(
        id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Delete tweet instance from bd.
    """
    self_id = request.headers.get('api-key')
    if not self_id:
        self_id = 1

    tweet = await Tweet.delete(
        user_id=self_id,
        tweet_id=id,
        session=session
    )
    if tweet:
        response = {"result": True}
        return JSONResponse(response, status_code=204)

    raise HTTPException(
        status_code=400,
        detail="Instance of tweet dont exist."
    )


@router.post(
    '/api/tweets/{id}/likes',
    tags=['Tweet'],
    response_model=Success,
)
async def post_likes(
        id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Add like to tweet.
    """
    self_id = request.headers.get('api-key')
    if not self_id:
        self_id = 1

    like = await Like.add_like(
        user_id=self_id,
        tweet_id=id,
        session=session,
    )
    if like:
        response = {"result": True}
        return JSONResponse(response, status_code=201)

    raise HTTPException(
        status_code=400,
        detail="Instance of tweet dont exist or user."
    )


@router.delete(
    '/api/tweets/{id}/likes',
    response_model=Success,
    tags=['Tweet']
)
async def delete_likes(
        id: int,
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Delete like from tweet.
    """
    self_id = request.headers.get('api-key')
    if not self_id:
        self_id = 1

    like = await Like.delete(
        user_id=self_id,
        tweet_id=id,
        session=session
    )

    if like:
        response = {"result": True}
        return JSONResponse(response, status_code=204)

    raise HTTPException(
        status_code=400,
        detail="Like instance dont exist."
    )
