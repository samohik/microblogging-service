from typing import List, Dict
from marshmallow import Schema, fields
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int
    name: str = "V",


class UserFollow(BaseModel):
    id: int
    name: str = "V",
    followers: list[User] = Field()
    following: list[User] = Field()


class GetUser(BaseModel):
    result: bool = True
    user: list[UserFollow] = Field()

