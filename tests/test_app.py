from app.models import User, Followed
from unittest.mock import patch
from twitter_handler import TwitterHandler
import pytest


def register(app, username, email, password):
    post = app.post('/register',
                    data=dict(username=username, email=email, password=password, confirm_password=password),
                    follow_redirects=True)
    return post


def login(app, username, password):
    post = app.post('/login', data=dict(username=username, password=password), follow_redirects=True)
    return post


def logout(app):
    get = app.get('/logout', follow_redirects=True)
    return get


def follow(app, username_follow):
    post = app.post('/follow', data=dict(username_follow=username_follow))
    return post


def unfollow(app, username_unfollow):
    post = app.post('/unfollow', data=dict(username_unfollow=username_unfollow))
    return post


def clear_follow_list(app):
    post = app.post('/clear_follow')
    return post


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
        assert user.check_password('test_pw')
        user.set_password(password)
        result = user.check_password(password)
        assert result == expected


def test_get_followed_users(client):
    with client.app_context():
        test_client = client.test_client()
        login(test_client, 'test_user', 'test_pw')
        user = User.query.filter_by(username='test_user').first()
        result = user.get_followed_users()
        assert len(result) == 1


def test_clear_follow_list(client):
    with client.app_context():
        test_client = client.test_client()
        login(test_client, 'test_user', 'test_pw')
        user = User.query.filter_by(username='test_user').first()
        user.clear_follow_list()
        result = user.get_followed_users()
        assert len(result) == 0


def test_home_page(client):
    with client.app_context():
        test_client = client.test_client()
        response = test_client.get('/', follow_redirects=True)
        assert response.status_code == 200
        assert b'Please login' in response.data
        response = login(test_client, 'test_user', 'test_pw')
        assert b'tweets by keyword' in response.data


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
        login(test_client, 'test_user', 'test_pw')
        response = logout(test_client)
        assert response.status_code == 200
        assert b'Logged out successfully' in response.data


@patch.object(TwitterHandler, 'verify_user_exists', return_value=True)
def test_add_followed(mock_handler, client):
    with client.app_context():
        test_client = client.test_client()
        register(test_client, 'test_follow', 'test@follow.com', 'follow')
        user = User.query.filter_by(username='test_follow').first()
        login(test_client, 'test_follow', 'follow')
        follow(test_client, 'test_followed_1')
        followed = Followed.query.filter_by(follower=user).all()
        assert len(followed) == 1
        assert user.username == 'test_follow'
        assert followed[0].username == 'test_followed_1'
        response = follow(test_client, 'test_followed_1')
        assert b'You already follow this user' in response.data


@patch.object(TwitterHandler, 'verify_user_exists', return_value=True)
def test_multiple_followers(mock_handler, client):
    with client.app_context():
        test_client = client.test_client()
        register(test_client, 'user_1', 'user1@user1.com', 'user_1')
        register(test_client, 'user_2', 'user2@user2.com', 'user_2')
        login(test_client, 'user_1', 'user_1')
        follow(test_client, 'followed')
        user = User.query.filter_by(username='user_1').first()
        followed = Followed.query.filter_by(follower=user).all()
        assert len(followed) == 1
        assert user.username == 'user_1'
        assert followed[0].username == 'followed'
        logout(test_client)
        login(test_client, 'user_2', 'user_2')
        follow(test_client, 'followed')
        user = User.query.filter_by(username='user_2').first()
        followed = Followed.query.filter_by(follower=user).all()
        assert len(followed) == 1
        assert user.username == 'user_2'
        assert followed[0].username == 'followed'


def test_remove_followed(client, user):
    with client.app_context():
        test_client = client.test_client()
        login(test_client, 'test_user', 'test_pw')
        followed = Followed.query.filter_by(follower=user).all()
        assert len(followed) == 1
        unfollow(test_client, 'test_followed_user')
        followed = Followed.query.filter_by(follower=user).all()
        assert len(followed) == 0


@patch.object(TwitterHandler, 'verify_user_exists', return_value=True)
def test_clear_follow_form(mock_handler, client):
    with client.app_context():
        test_client = client.test_client()
        login(test_client, 'test_user', 'test_pw')
        follow(test_client, 'user_1')
        follow(test_client, 'user_2')
        user = User.query.filter_by(username='test_user').first()
        assert len(user.get_followed_users()) == 3
        clear_follow_list(test_client)
        assert len(user.get_followed_users()) == 0
