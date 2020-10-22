from flask import Flask
from config import Config
from app.main import bp as main_bp
from app.auth import bp as auth_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    return app
