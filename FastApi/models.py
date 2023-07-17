from typing import List, Dict, Any
from datetime import datetime


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    Integer,
    Column,
    String,
    ForeignKey,
    DateTime,
    BLOB,
    select,
    Text
)
from sqlalchemy.orm import relationship, backref, selectinload

from auth.models import User
from database import Base


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
    async def get_follow(
            cls,
            session: AsyncSession,
            from_user: int,
            to_user: int,
    ):
        query = select(cls).where(
            cls.to_user_id == to_user,
            cls.from_user_id == from_user,
        ).options(
            selectinload(cls.to_user),
            selectinload(cls.from_user),
        )
        data = (await session.execute(query)).scalars().first()
        print(data)
        result = {}
        if data:
            result["to"] = data.to_user.id
            result["from"] = data.from_user.id
        return result

    @classmethod
    async def get_follower(
            cls,
            session: AsyncSession,
            id: int,
    ) -> List[Dict]:
        query = select(cls).where(
            cls.to_user_id == id
        ).options(
            selectinload(cls.to_user),
            selectinload(cls.from_user),
        )
        data = (await session.execute(query)).scalars().all()
        result = []
        if data:
            result = [
                {'id': x.from_user.id, 'name': x.from_user.name}
                for x in data
            ]
        return result

    @classmethod
    async def get_following(
            cls,
            session: AsyncSession,
            id: int,
    ) -> List[Dict]:
        query = select(cls).where(
            cls.from_user_id == id
        ).options(
            selectinload(cls.to_user),
            selectinload(cls.from_user),
        )
        data = (await session.execute(query)).scalars().all()
        result = []
        if data:
            result = [
                {'id': x.to_user.id, 'name': x.to_user.name}
                for x in data
            ]
        return result

    @classmethod
    async def handler_follower(
            cls,
            session: AsyncSession,
            method: str,
            to_user_id: int = 4,
            from_user_id: int = 1,
    ) -> bool:
        result = False
        user_exist = await User.get_user(
            id=to_user_id,
            session=session,
        )
        if user_exist:
            query = select(Follow).filter(
                Follow.to_user_id == to_user_id,
                Follow.from_user_id == from_user_id,
            ).options(
                selectinload(Follow.to_user),
                selectinload(Follow.from_user),
            )
            already_exist = (await session.execute(query)).scalars().first()
            if method == "POST" and not already_exist:
                result = await Follow.add_follower(
                    session=session,
                    to_user_id=to_user_id,
                    from_user_id=from_user_id,
                )
            elif method == "DELETE" and already_exist:
                result = await Follow.delete_follower(
                    session=session,
                    item=already_exist,
                )
        return result

    @classmethod
    async def add_follower(
            cls,
            session: AsyncSession,
            to_user_id,
            from_user_id
    ):
        follower = Follow(
            to_user_id=to_user_id,
            from_user_id=from_user_id,
        )
        session.add(follower)
        await session.commit()
        return True

    @classmethod
    async def delete_follower(
            cls,
            session: AsyncSession,
            item,
    ):
        await session.delete(item)
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
    async def get_like(
            cls,
            session: AsyncSession,
            user_id: int,
            tweet_id: int
    ) -> Any | bool:
        query = select(Like).where(
            Like.user_id == user_id,
            Like.tweet_id == tweet_id,
        ).options(
            selectinload(cls.tweet_backref),
            selectinload(cls.user_backref),
        )
        res = (await session.execute(query)).scalars().first()
        if res:
            return res
        return False

    @classmethod
    async def get_likes(
            cls,
            session: AsyncSession,
            tweet_id: int
    ) -> List:
        query = select(Like).filter(
            Like.tweet_id == tweet_id
        ).options(
            selectinload(cls.user_backref),
            selectinload(cls.tweet_backref),
        )
        res = (await session.execute(query)).scalars().all()
        return res

    @classmethod
    async def add_like(
            cls,
            session: AsyncSession,
            user_id: int,
            tweet_id: int
    ) -> bool:
        user = await User.get_user(
            session=session,
            id=user_id,
        )
        tweet = await Tweet.get_tweet(
            tweet_id=tweet_id,
            session=session,
        )
        if user and tweet:
            like_exist = await Like.get_like(
                session=session,
                user_id=user_id,
                tweet_id=tweet_id,
            )
            if not like_exist:
                like = Like(
                    user_id=user_id,
                    tweet_id=tweet_id,
                )
                session.add(like)
                await session.commit()
                return True
        return False

    @classmethod
    async def delete(
            cls,
            session: AsyncSession,
            user_id: int,
            tweet_id: int
    ) -> bool:

        like = await Like.get_like(
            session=session,
            user_id=user_id,
            tweet_id=tweet_id,
        )
        if like:
            await session.delete(like)
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
    async def get_tweet(
            cls,
            session: AsyncSession,
            tweet_id: int
    ) -> Any:
        res = await session.get(Tweet, tweet_id)
        return res

    @classmethod
    async def get_tweets(
            cls,
            session: AsyncSession,
            user_id: int
    ) -> List[Any, ]:
        query = select(cls).where(
            Tweet.user_id == user_id,
        )
        res = (await session.execute(query)).scalars().all()
        return res

    @classmethod
    async def add_tweet(
            cls,
            session: AsyncSession,
            user_id: int,
            content: str
    ) -> Any | bool:
        user = await User.get_user(
            id=user_id,
            session=session,
        )
        if user:
            tweet = Tweet(
                content=content,
                user_id=user_id,
            )
            session.add(tweet)
            await session.flush()
            return tweet
        return False

    @classmethod
    async def delete(
            cls,
            session: AsyncSession,
            user_id: int,
            tweet_id: int
    ) -> bool:
        tweet = await Tweet.get_tweet(
            tweet_id=tweet_id,
            session=session,
        )
        if tweet:
            if tweet.user_id == user_id:
                await session.delete(tweet)
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
