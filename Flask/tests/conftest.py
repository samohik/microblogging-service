import pytest

from Flask.main import create_app
from Flask.models import db as _db, User, Follow, Tweet, Like


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    with _app.app_context():
        _db.create_all()

        # Users
        user_me = User(name="Jonny")
        user_id_2 = User(
            name="V",
        )
        user_id_3 = User(
            name="Alt",
        )
        user_id_4 = User(
            name="Jade",
        )
        _db.session.add(user_me)
        _db.session.add(user_id_2)
        _db.session.add(user_id_3)
        _db.session.add(user_id_4)
        _db.session.flush()

        # Subscribers
        follower_me = Follow(
            to_user_id=user_me.id,
            from_user_id=user_id_3.id,
        )

        # Am signed to
        following_me = Follow(
            to_user_id=user_id_2.id,
            from_user_id=user_me.id,
        )
        following_2 = Follow(
            to_user_id=user_id_4.id,
            from_user_id=user_id_2.id,
        )

        # Tweet
        tweet_me = Tweet(
            content='Test',
            user_id=user_me.id,
        )
        tweet_user_2 = Tweet(
            content='Test2',
            user_id=user_id_2.id,
        )

        _db.session.add(follower_me)
        _db.session.add(following_me)
        _db.session.add(following_2)
        _db.session.add(tweet_me)
        _db.session.add(tweet_user_2)
        _db.session.flush()

        # Like
        like_to_user_2 = Like(
            user_id=user_me.id,
            tweet_id=tweet_user_2.id,
        )
        like_from_user_2 = Like(
            user_id=user_id_2.id,
            tweet_id=tweet_me.id,
        )
        like_from_user_4 = Like(
            user_id=user_id_4.id,
            tweet_id=tweet_me.id,
        )

        _db.session.add(like_to_user_2)
        _db.session.add(like_from_user_2)
        _db.session.add(like_from_user_4)
        _db.session.commit()

        yield _app

        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
