import pytest

from Flask.main import create_app
from Flask.models import db as _db, User, Follower


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    with _app.app_context():
        _db.create_all()
        user_1 = User(
            name="Jonny"
        )
        follower = User(
            name="Kate",
        )
        # following = User(
        #     name="V",
        # )
        # fr = Follower(
        #     user_id=1,
        #     follower_id=follower,
        # )
        # user_1.follower = fr
        # fing = Follower(
        #     user_id=1
        # )

        _db.session.add(user_1)
        # _db.session.add(following)
        # _db.session.add(follower)
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
