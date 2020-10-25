from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    password_hash = db.Column(db.String(100))
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        return f'<User> {self.username}'
