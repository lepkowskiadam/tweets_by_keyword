from flask import render_template, flash, redirect, url_for
from app import db
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import FollowUserForm
from app.models import Followed


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = FollowUserForm()
    title = 'tweets by keyword'
    if form.validate_on_submit():
        follow = Followed(username=form.username.data, follower=current_user)
        db.session.add(follow)
        db.session.commit()
        flash(f'You are now following {form.username.data}')
        return redirect(url_for('main.index'))
    return render_template('index.html', title=title, form=form)
