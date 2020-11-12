from config import Config
from app import create_app, db
from app.models import User, Followed
import pytest


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    TESTING = True


def register(app, username, email, password):
    post = app.post('/register',
                    data=dict(username=username, email=email, password=password, confirm_password=password),
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


def test_home_page(client):
    with client.app_context():
        test_client = client.test_client()
        response = test_client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert b'Please login' in response.data


@pytest.mark.parametrize('username, email, password, expected_msg, expected_users', [
    ('test_1', 'test1@test.com', 'some_pw', b'Registered successfully', 2),
    ('test_user', 'test_taken_username@test.com', 'some_pw', b'Username already taken', 1),
    ('test_taken_email', 'test@test.com', 'some_pw', b'Email already registered', 1),
])
def test_registration_form(client, username, email, password, expected_msg, expected_users):
    with client.app_context():
        test_client = client.test_client()
        response = register(test_client, username, email, password)
        assert response.status_code == 200
        assert expected_msg in response.data
        u = User.query.all()
        assert len(u) == expected_users


@pytest.mark.parametrize('username, password, expected_msg, expected_status', [
    ('test_user', 'test_pw', b'Logged in successfully', 200),
    ('wrong_username', 'test_pw', b'Invalid username or password', 200),
    ('test_user', 'wrong_pw', b'Invalid username or password', 200)
])
def test_login_form(client, username, password, expected_msg, expected_status):
    with client.app_context():
        test_client = client.test_client()
        response = login(test_client, username, password)
        assert response.status_code == expected_status
        assert expected_msg in response.data


def test_logout(client):
    with client.app_context():
        test_client = client.test_client()
        response = logout(test_client)
        assert response.status_code == 200
        assert b'Logged out successfully' in response.data
