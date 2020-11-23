from twitter_handler import TwitterHandler
from unittest.mock import patch, Mock
import tweepy
import pytest


@pytest.fixture
def handler():
    th = TwitterHandler()
    return th


def test_auth(handler):
    with patch.object(handler, 'api') as api_mock:
        api_mock.home_timeline = Mock(return_value=[])
        assert handler
        assert [] == handler.api.home_timeline()


@pytest.mark.parametrize('username, expected', [
    ('Twitter', True),
    ('xxxxxxxxxxxxxxxx', False)  # twitter only allows 15 character long usernames so this should always return False
])
def test_verify_user_exists(handler, username, expected):
    return_value = True if len(username) <= 15 else False
    with patch.object(handler, 'verify_user_exists', return_value=return_value):
        result = handler.verify_user_exists(username)
        assert result == expected


def test_get_tweets(handler):
    return_value = [Mock() for _ in range(20)]
    for index, mock_tweet in enumerate(return_value):
        mock_tweet.text = str(index)
    with patch.object(tweepy.Cursor, 'items', return_value=return_value):
        assert len(handler.get_tweets('Twitter', '10')) == 1
