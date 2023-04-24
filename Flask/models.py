from datetime import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)

    @classmethod
    def get_me(cls):
        return db.session.query(User).first()


class Follower(db.Model):
    __tablename__ = "follower"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.ForeignKey("user.id"),)
    user_backref = db.relationship(
        "User",
        backref=db.backref(
            "follower",
            cascade="all, delete-orphan",
        ),
        passive_deletes=True,
        lazy="select",
    )

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)


class Following(db.Model):
    __tablename__ = "following"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.ForeignKey("user.id"),)
    client = db.relationship(
        "User",
        backref=db.backref(
            "following",
            cascade="all, delete-orphan",
        ),
        passive_deletes=True,
        lazy="select",
    )

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)


class Tweet(db.Model):
    __tablename__ = "tweet"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.ForeignKey("user.id"),)
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


class Test(db.Model):
    __tablename__ = "test"

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    follower_id = db.Column(db.ForeignKey("user.id"),)
    following_id = db.Column(db.ForeignKey("user.id"),)

    def __repr__(self):
        return "Id: {id}\nCreated: {created}".format(id=self.id, created=self.created)

    @classmethod
    def get_all(cls):
        return db.session.query(Test).first()
