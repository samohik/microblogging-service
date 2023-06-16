import json
from datetime import datetime
from typing import List, Dict, Any, Tuple, Type

from sqlalchemy import *
from sqlalchemy.orm import relationship, backref

from FastApi.database import Base, async_session


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(80))

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)

    @classmethod
    async def get_user(cls, id=1) -> dict[str, Any]:
        async with async_session() as session:
            data = await session.get(User, id)
            result = {}
            if data:
                result['id'] = data.id
                result['name'] = data.name
            return result


class Follow(Base):
    __tablename__ = "follow"

    id = Column(Integer, primary_key=True)

    to_user_id = Column(ForeignKey('user.id'))
    to_user = relationship(
        'User', lazy="select", foreign_keys=[to_user_id],
        backref='following'
    )

    from_user_id = Column(ForeignKey('user.id'))
    from_user = relationship(
        'User', lazy="select", foreign_keys=[from_user_id],
        backref='followers'
    )

    def __repr__(self):
        return "Follower: {}\nFollowing: {}".format(self.to_user_id, self.from_user_id)

    @classmethod
    async def get_follow(cls, from_user, to_user):
        async with async_session() as session:
            data = await session.query(Follow).filter(
                Follow.to_user_id == to_user,
                Follow.from_user_id == from_user,
            ).first()
            result = {}
            if data:
                result["to"] = data.to_user.id
                result["from"] = data.from_user.id
            return result

    @classmethod
    async def get_follower(cls, id=1) -> List[Dict]:
        async with async_session() as session:
            data = await session.query(Follow).filter(Follow.to_user_id == id)
            result = []
            if data:
                result = [
                    {'id': x.from_user.id, 'name': x.from_user.name}
                    for x in data
                ]
            return result

    @classmethod
    async def get_following(cls, id=1) -> List[Dict]:
        async with async_session() as session:
            data = await session.query(Follow).filter(Follow.from_user_id == id)
            result = []
            if data:
                result = [
                    {'id': x.to_user.id, 'name': x.to_user.name}
                    for x in data
                ]
            return result

    @classmethod
    async def handler_follower(cls, method: str, to_user_id=4, from_user_id=1, ) -> bool:
        result = False
        user_exist = User.get_user(to_user_id)
        if user_exist:
            async with async_session() as session:
                already_exist = await session.query(Follow).filter(
                    Follow.to_user_id == to_user_id,
                    Follow.from_user_id == from_user_id,
                ).first()
                if method == "POST" and not already_exist:
                    result = await Follow.add_follower(
                        to_user_id=to_user_id,
                        from_user_id=from_user_id,
                    )
                elif method == "DELETE" and already_exist:
                    result = await Follow.delete_follower(already_exist)
        return result

    @classmethod
    async def add_follower(cls, to_user_id, from_user_id):
        async with async_session() as session:
            follower = Follow(
                to_user_id=to_user_id,
                from_user_id=from_user_id,
            )
            session.add(follower)
            await session.commit()
            return True

    @classmethod
    async def delete_follower(cls, item):
        async with async_session() as session:
            session.delete(item)
            await session.commit()
            return True


class Like(Base):
    __tablename__ = 'like'

    id = Column(Integer, primary_key=True)

    user_id = Column(
        ForeignKey("user.id"),
    )
    user_backref = relationship(
        "User",
        backref=backref(
            "like",
            cascade="all, delete-orphan",
        ),
        passive_deletes=True,
        lazy="select",
    )
    tweet_id = Column(
        ForeignKey("tweet.id"),
    )
    tweet_backref = relationship(
        "Tweet",
        backref=backref(
            "like",
            cascade="all, delete-orphan",
        ),
        passive_deletes=True,
        lazy="select",
    )

    def __str__(self):
        return str(self.id)

    @classmethod
    async def get_like(cls, user_id: int, tweet_id: int) -> Any | bool:
        async with async_session() as session:
            res = await session.query(Like).filter(
                Like.user_id == user_id,
                Like.tweet_id == tweet_id,
            ).first()
            if res:
                return res
            return False

    @classmethod
    async def get_likes(cls, tweet_id: int) -> List:
        async with async_session() as session:
            res = await session.query(Like).filter(Like.tweet_id == tweet_id).all()
            return res

    @classmethod
    async def add_like(cls, user_id: int, tweet_id: int) -> bool:
        user = await User.get_user(user_id)
        tweet = await Tweet.get_tweet(tweet_id)
        if user and tweet:
            like_exist = Like.get_like(
                user_id=user_id,
                tweet_id=tweet_id,
            )
            if not like_exist:
                async with async_session() as session:
                    like = Like(
                        user_id=user_id,
                        tweet_id=tweet_id,
                    )
                    session.add(like)
                    await session.commit()
                    return True
        return False

    @classmethod
    async def delete(cls, user_id: int, tweet_id: int) -> bool:

        like = await Like.get_like(user_id, tweet_id)
        if like:
            async with async_session() as session:
                session.delete(like)
                await session.commit()
                return True
        return False


class Tweet(Base):
    __tablename__ = "tweet"

    id = Column(Integer, primary_key=True)
    content = Column(String(280), nullable=False)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)

    user_id = Column(
        ForeignKey("user.id"),
    )
    user_backref = relationship(
        "User",
        backref=backref(
            "tweet",
            cascade="all, delete-orphan",
        ),
        passive_deletes=True,
        lazy="select",
    )

    def __repr__(self):
        return str(self.id)

    @classmethod
    async def get_tweet(cls, tweet_id: int) -> Any:
        async with async_session() as session:
            res = await session.get(Tweet, tweet_id)
            return res

    @classmethod
    async def get_tweets(cls, user_id: int) -> List[Any, ]:
        async with async_session() as session:
            res = await session.query(Tweet).filter(
                Tweet.user_id == user_id,
            ).all()
            return res

    @classmethod
    async def add_tweet(cls, user_id: int, content: str) -> Any | bool:
        user = User.get_user(user_id)
        if user:
            async with async_session() as session:
                tweet = Tweet(
                    content=content,
                    user_id=user_id,
                )
                session.add(tweet)
                await session.flush()
                return tweet
        return False

    @classmethod
    async def delete(cls, user_id: int, tweet_id: int) -> bool:
        tweet = Tweet.get_tweet(tweet_id=tweet_id)
        if tweet:
            if tweet.user_id == user_id:
                async with async_session() as session:
                    session.delete(tweet)
                    await session.commit()
                    return True
        return False


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    data = Column(BLOB)

    tweet_id = Column(ForeignKey("tweet.id"))
    media_backref = relationship(
        "Tweet",
        backref=backref(
            "media",
            cascade="all, delete-orphan",
        ),
        passive_deletes=True,
        lazy="select",
    )

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)