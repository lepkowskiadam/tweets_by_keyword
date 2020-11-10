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

    with app.app_context():
        db.create_all()
        user = User(username='test_user', email='test@test.com')
        user.set_password('test_pw')
        followed = Followed(username='test_followed_user', follower=user)
        db.session.add(user)
        db.session.add(followed)
        db.session.commit()
    return app


def test_client(client):
    with client.app_context():
        u = User.query.all()
        f = Followed.query.all()
        assert u[0].username == 'test_user'
        assert f[0].username == 'test_followed_user'
        assert u[0].followed.one() == f[0]
        assert len(u) == 1
        assert len(f) == 1
