from typing import List, Dict
from marshmallow import Schema, fields
from pydantic import BaseModel, Field


class Author(BaseModel):
    id: int
    name: str = 'John Doe'


class Likes(BaseModel):
    user_id: int = 0
    name: str = 'Foe'


class TweetList(BaseModel):
    id: int = Field(default=0, examples=[2])
    content: str = Field(default='Test')
    attachments: list = Field(examples=[])
    author: Author


class TweetGet(BaseModel):
    result: bool = Field(default=True)
    tweets: list[TweetList] = Field(examples=[])
    likes: list[Likes] = Field()


class TweetPost(BaseModel):
    tweet_data: str = "Test"
    # tweet_media_ids: List[int] = Field()


class TweetPostSuccess(BaseModel):
    result: bool = True
    tweet_id: int


class TweetSchema(Schema):
    tweet_data = fields.String(required=True)
    tweet_media_ids = fields.Dict(required=False)
