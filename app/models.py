from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from twitter_handler import TwitterHandler


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(300))
    email = db.Column(db.String(120), index=True, unique=True)
    followed = db.relationship('Followed', backref='follower', lazy='dynamic')

    def __repr__(self):
        return f'<User> {self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_followed_users(self):
        return [followed.username for followed in self.followed.all()]

    def clear_follow_list(self):
        for followed in self.followed.all():
            db.session.delete(followed)
        db.session.commit()

    def tweets_from_followed(self, keyword):
        results = []
        for followed in self.followed.all():
            results.append((followed.username, TwitterHandler.get_tweets(followed.username, keyword)))
        return results


class Followed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Twitter_user: {self.username}'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
