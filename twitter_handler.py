from dotenv import load_dotenv
import tweepy
import os

load_dotenv()


class TwitterHandler:
    consumer_key = os.getenv('CONSUMER_KEY')
    secret_key = os.getenv('SECRET_KEY')
    access_token = os.getenv('ACCESS_TOKEN')
    access_secret_token = os.getenv('ACCESS_SECRET_TOKEN')

    def __init__(self):
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.secret_key)
        self.auth.set_access_token(self.access_token, self.access_secret_token)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def verify_user_exists(self, username):
        try:
            self.api.get_user(username)
        except tweepy.error.TweepError:
            return False
        return True

    def get_tweets(self, username, keyword):
        if self.verify_user_exists(username):
            tweets = []
            for tweet in tweepy.Cursor(self.api.user_timeline, screen_name=username).items(20):
                if keyword.lower() in tweet.text.lower():
                    tweets.append((tweet.text, tweet.id))
            return tweets
        return f'{username} not found'
