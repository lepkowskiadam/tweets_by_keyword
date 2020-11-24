from flask import render_template, flash, redirect, url_for
from app import db
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import FollowUserForm, UnfollowUserForm
from app.models import Followed


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    follow_form = FollowUserForm()
    unfollow_form = UnfollowUserForm()
    title = 'tweets by keyword'
    follow_form.validate_on_submit()
    if follow_form.follow_submit.data and follow_form.validate():
        follow = Followed(username=follow_form.username.data, follower=current_user)
        db.session.add(follow)
        db.session.commit()
        flash(f'You are now following {follow_form.username.data}')
        return redirect(url_for('main.index'))
    elif unfollow_form.unfollow_submit.data and unfollow_form.validate():
        followed = Followed.query.filter_by(username=unfollow_form.username.data, follower=current_user).first()
        db.session.delete(followed)
        db.session.commit()
        flash(f'You no longer follow {unfollow_form.username.data}')
        return redirect(url_for('main.index'))
    return render_template('index.html', title=title, follow_form=follow_form, unfollow_form=unfollow_form)
