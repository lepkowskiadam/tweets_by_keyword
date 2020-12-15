import os

from dotenv import load_dotenv
import tweepy


load_dotenv()


class TwitterHandler:
    consumer_key = os.getenv('CONSUMER_KEY')
    secret_key = os.getenv('SECRET_KEY')
    access_token = os.getenv('ACCESS_TOKEN')
    access_secret_token = os.getenv('ACCESS_SECRET_TOKEN')
    auth = tweepy.OAuthHandler(consumer_key, secret_key)
    auth.set_access_token(access_token, access_secret_token)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    @classmethod
    def verify_user_exists(cls, username):
        try:
            cls.api.get_user(username)
        except tweepy.error.TweepError:
            return False
        return True

    @classmethod
    def get_tweets(cls, username, keyword):
        if cls.verify_user_exists(username):
            tweets = []
            for tweet in tweepy.Cursor(cls.api.user_timeline, screen_name=username).items(20):
                if keyword.lower() in tweet.text.lower():
                    tweets.append(tweet.text)
            return tweets
        return f'{username} not found'
