from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), )

    def __repr__(self):
        return "Id: {id}\nName: {name}".format(id=self.id, name=self.name)

    @classmethod
    def get_me(cls):
        return db.session.query(
            User
        ).first()


class Follower(db.Model):
    __tablename__ = "follower"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), )
    user_id = db.Column(db.ForeignKey("user.id", ondelete="CASCADE"), )
    client = db.relationship(
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
    name = db.Column(db.String(80), )
    user_id = db.Column(
        db.ForeignKey("user.id", ondelete="CASCADE"),
    )
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
