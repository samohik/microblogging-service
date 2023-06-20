from pydantic import BaseModel


class TweetSchema(BaseModel):
    tweet_data: str
    tweet_media_ids: str

    class Config:
        orm_mode = True