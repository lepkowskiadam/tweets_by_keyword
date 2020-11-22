from twitter_handler import TwitterHandler
import pytest


@pytest.fixture
def handler():
    th = TwitterHandler()
    return th


def test_auth(handler):
    assert handler
    assert [] == handler.api.home_timeline()


@pytest.mark.parametrize('username, expected', [
    ('Twitter', True),
    ('xxxxxxxxxxxxxxxx', False)  # twitter only allows 15 character long usernames so this will always return False
])
def test_verify_user_exists(handler, username, expected):
    result = handler.verify_user_exists(username)
    assert result == expected
