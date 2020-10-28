from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from app.models import User
from app.auth import bp as auth_bp
from app.auth.forms import LoginForm


@auth_bp.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form, title='Sign in')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
