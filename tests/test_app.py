from config import Config
from app import create_app, db
from app.models import User, Followed
import pytest


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


@pytest.fixture
def client():
    app = create_app(TestConfig)
    app.testing = True

    client = app.test_client()
    with app.app_context():
        db.create_all()
        user = User(username='test_user', email='test@test.com')
        user.set_password('test_pw')
        followed = Followed(username='test_followed_user', user_id=user.id)
        db.session.add(user)
        db.session.add(followed)
        db.session.commit()
    yield client


def test_client(client):
    assert client