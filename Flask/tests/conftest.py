import pytest

from Flask.main import create_app
from Flask.models import db as _db, User, Followers, Following


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    with _app.app_context():
        _db.create_all()

        user_me = User(name="Jonny")

        # users
        user_id_2 = User(
            name="V",
        )
        user_id_3 = User(
            name="Alt",
        )

        # connections
        following = Following(
            id=user_id_2.id,
            name=user_id_2.name,
            user_id=user_me.id,
        )
        followers = Followers(
            id=user_id_3.id,
            name=user_id_3.name,
            user_id=user_me.id,
        )

        _db.session.add(user_me)
        _db.session.add(user_id_3)
        _db.session.add(user_id_2)
        _db.session.add(followers)
        _db.session.add(following)
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
