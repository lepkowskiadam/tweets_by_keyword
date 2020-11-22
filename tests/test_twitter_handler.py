from twitter_handler import TwitterHandler
import pytest


@pytest.fixture
def handler():
    th = TwitterHandler()
    return th


def test_auth(handler):
    assert handler
    assert [] == handler.api.home_timeline()

