from app import create_app, db
from app.models import User, Followed
from config import Config
from twitter_handler import TwitterHandler
import pytest


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    TESTING = True


@pytest.fixture
def handler():
    return TwitterHandler


@pytest.fixture
def client():
    app = create_app(TestConfig)
    app.testing = True

    with app.app_context():
        db.create_all()
        user = User(username='test_user', email='test@test.com')
        user.set_password('test_pw')
        followed = Followed(username='test_followed_user', follower=user)
        db.session.add(user)
        db.session.add(followed)
        db.session.commit()
    return app


@pytest.fixture
def user(client):
    with client.app_context():
        u = User.query.filter_by(username='test_user').first()
    return u
