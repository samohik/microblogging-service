import json
from datetime import datetime
from typing import List, Dict, Any, Tuple, Type

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)

    @classmethod
    def get_user(cls, id=1) -> dict[str, Any]:
        data = db.session.get(User, id)
        result = {}
        if data:
            result['id'] = data.id
            result['name'] = data.name
        return result


class Follow(db.Model):
    __tablename__ = "follow"

    id = db.Column(db.Integer, primary_key=True)

    to_user_id = db.Column(db.ForeignKey('user.id'))
    to_user = db.relationship(
        'User', lazy="select", foreign_keys=[to_user_id],
        backref='following'
    )

    from_user_id = db.Column(db.ForeignKey('user.id'))
    from_user = db.relationship(
        'User', lazy="select", foreign_keys=[from_user_id],
        backref='followers'
    )

    def __repr__(self):
        return "Follower: {}\nFollowing: {}".format(self.to_user_id, self.from_user_id)

    @classmethod
    def get_follow(cls, from_user, to_user):
        data = db.session.query(Follow).filter(
            Follow.to_user_id == to_user,
            Follow.from_user_id == from_user,
        ).first()
        result = {}
        if data:
            result["to"] = data.to_user.id
            result["from"] = data.from_user.id
        return result

    @classmethod
    def get_follower(cls, id=1) -> List[Dict]:
        data = db.session.query(Follow).filter(Follow.to_user_id == id)
        result = []
        if data:
            result = [
                {'id': x.from_user.id, 'name': x.from_user.name}
                for x in data
            ]
        return result

    @classmethod
    def get_following(cls, id=1) -> List[Dict]:
        data = db.session.query(Follow).filter(Follow.from_user_id == id)
        result = []
        if data:
            result = [
                {'id': x.to_user.id, 'name': x.to_user.name}
                for x in data
            ]
        return result

    @classmethod
    def handler_follower(cls, method: str, to_user_id=4, from_user_id=1, ) -> bool:
        result = False
        user_exist = User.get_user(to_user_id)
        if user_exist:
            already_exist = db.session.query(Follow).filter(
                Follow.to_user_id == to_user_id,
                Follow.from_user_id == from_user_id,
            ).first()
            if method == "POST" and not already_exist:
                result = Follow.add_follower(
                    to_user_id=to_user_id,
                    from_user_id=from_user_id,
                )
            elif method == "DELETE" and already_exist:
                result = Follow.delete_follower(already_exist)
        return result

    @classmethod
    def add_follower(cls, to_user_id, from_user_id):
        follower = Follow(
            to_user_id=to_user_id,
            from_user_id=from_user_id,
        )
        db.session.add(follower)
        return True

    @classmethod
    def delete_follower(cls, item):
        db.session.delete(item)
        return True


class Like(db.Model):
    __tablename__ = 'like'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.ForeignKey("user.id"),
    )
    user_backref = db.relationship(
        "User",
        backref=db.backref(
            "like",
            cascade="all, delete-orphan",
        ),
        passive_deletes=True,
        lazy="select",
    )
    tweet_id = db.Column(
        db.ForeignKey("tweet.id"),
    )
    tweet_backref = db.relationship(
        "Tweet",
        backref=db.backref(
            "like",
            cascade="all, delete-orphan",
        ),
        passive_deletes=True,
        lazy="select",
    )

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_like(cls, user_id: int, tweet_id: int) -> Any | bool:
        res = db.session.query(Like).filter(
            Like.user_id == user_id,
            Like.tweet_id == tweet_id,
        ).first()
        if res:
            return res
        return False

    @classmethod
    def get_likes(cls, tweet_id: int) -> List:
        res = db.session.query(Like).filter(Like.tweet_id == tweet_id).all()
        return res

    @classmethod
    def add_like(cls, user_id: int, tweet_id: int) -> bool:
        user = User.get_user(user_id)
        tweet = Tweet.get_tweet(tweet_id)
        if user and tweet:
            like_exist = Like.get_like(
                user_id=user_id,
                tweet_id=tweet_id,
            )
            if not like_exist:
                like = Like(
                    user_id=user_id,
                    tweet_id=tweet_id,
                )
                db.session.add(like)
                return True
        return False

    @classmethod
    def delete(cls, user_id: int, tweet_id: int) -> bool:

        like = Like.get_like(user_id, tweet_id)
        if like:
            db.session.delete(like)
            return True
        return False


class Tweet(db.Model):
    __tablename__ = "tweet"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(
        db.ForeignKey("user.id"),
    )
    user_backref = db.relationship(
        "User",
        backref=db.backref(
            "tweet",
            cascade="all, delete-orphan",
        ),
        passive_deletes=True,
        lazy="select",
    )

    def __repr__(self):
        return str(self.id)

    @classmethod
    def get_tweet(cls, tweet_id: int) -> Any:
        res = db.session.get(Tweet, tweet_id)
        return res

    @classmethod
    def get_tweets(cls, user_id: int) -> List[Any, ]:
        res = db.session.query(Tweet).filter(
            Tweet.user_id == user_id,
        ).all()
        return res

    @classmethod
    def add_tweet(cls, user_id: int, content: str) -> Any | bool:
        user = User.get_user(user_id)
        if user:
            tweet = Tweet(
                content=content,
                user_id=user_id,
            )
            db.session.add(tweet)
            db.session.flush()

            return tweet
        return False

    @classmethod
    def delete(cls, user_id: int, tweet_id: int) -> bool:
        tweet = Tweet.get_tweet(tweet_id=tweet_id)
        if tweet:
            if tweet.user_id == user_id:
                db.session.delete(tweet)
                return True
        return False


class Media(db.Model):
    __tablename__ = "media"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    data = db.Column(db.BLOB)

    tweet_id = db.Column(db.ForeignKey("tweet.id"))
    media_backref = db.relationship(
        "Tweet",
        backref=db.backref(
            "media",
            cascade="all, delete-orphan",
        ),
        passive_deletes=True,
        lazy="select",
    )

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)
