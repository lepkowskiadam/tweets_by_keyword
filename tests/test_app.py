from config import Config
from app import create_app, db
from app.models import User, Followed
import pytest


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    TESTING = True


def register(app, username, email, password):
    post = app.post('/register', data=dict(username=username, email=email, password=password, confirm_password=password),
                    follow_redirects=True)
    return post


def login(app, username, password):
    post = app.post('/login', data=dict(username=username, password=password), follow_redirects=True)
    return post


def logout(app):
    get = app.get('logout', follow_redirects=True)
    return get


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


def test_app(client):
    with client.app_context():
        u = User.query.all()
        f = Followed.query.all()
        assert u[0].username == 'test_user'
        assert f[0].username == 'test_followed_user'
        assert u[0].followed.one() == f[0]
        assert len(u) == 1
        assert len(f) == 1


@pytest.mark.parametrize('password, expected', [
    ('test_pw', True),
    ('wrong_password', False)
])
def test_pw_hash(client, user, password, expected):
    with client.app_context():
        result = user.check_password(password)
        assert result == expected


@pytest.mark.parametrize('password, expected', [
    ('password_1', True),
    ('password_2', True)
])
def test_set_pw(client, user, password, expected):
    with client.app_context():
        user.set_password(password)
        result = user.check_password(password)
        assert result == expected


def test_registration(client):
    with client.app_context():
        client_test = client.test_client()
        response = register(client_test, 'test_1', 'test@test2.com', 'some_pw')
        assert response.status_code == 200
        assert b'Registered successfully' in response.data
        u = User.query.all()
        assert len(u) == 2