from flask import render_template, flash, redirect, url_for
from app.auth import bp as auth_bp
from app.auth.forms import LoginForm


@auth_bp.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'{form.username.data} loggin in, remember_me={form.remember_me.data}')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form, title='Sign in')