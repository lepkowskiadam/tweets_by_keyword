from flask import render_template
from app.auth import bp as auth_bp
from app.auth.forms import LoginForm


@auth_bp.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form, title='Sign in')