from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    followers = db.relationship(
        "Followers", backref=db.backref("user", lazy="joined")
    )
    following = db.relationship(
        "Following", backref=db.backref("user", lazy="joined")
    )

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)

    @classmethod
    def get_me(cls):
        return db.session.query(
            User.id,
            User.name,
            User.followers,
            User.following,
        ).first()


class Followers(db.Model):
    __tablename__ = "followers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    user_id = db.Column(
        db.ForeignKey("user.id"),
    )

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)


class Following(db.Model):
    __tablename__ = "following"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    user_id = db.Column(
        db.ForeignKey("user.id"),
    )

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)


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
        return "Id: {id}}".format(id=self.id)


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
