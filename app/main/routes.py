from flask import render_template, flash, redirect, url_for
from app import db
from flask_login import login_required, current_user
from app.main import bp
from app.main.forms import FollowUserForm, UnfollowUserForm, BlankForm
from app.models import Followed, User


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    follow_form = FollowUserForm()
    unfollow_form = UnfollowUserForm()
    clear_form = BlankForm()
    title = 'tweets by keyword'
    return render_template('index.html', title=title, follow_form=follow_form,
                           unfollow_form=unfollow_form, clear_form=clear_form)


@bp.route('/follow', methods=['GET', 'POST'])
@login_required
def follow():
    follow_form = FollowUserForm()
    unfollow_form = UnfollowUserForm()
    clear_form = BlankForm()
    title = 'tweets by keyword'
    if follow_form.validate_on_submit():
        follow_user = Followed(username=follow_form.username_follow.data,
                               follower=current_user)
        db.session.add(follow_user)
        db.session.commit()
        flash(f'You are now following {follow_form.username_follow.data}')
        return redirect(url_for('main.index'))
    return render_template('index.html', title=title, follow_form=follow_form,
                           unfollow_form=unfollow_form, clear_form=clear_form)


@bp.route('/unfollow', methods=['GET', 'POST'])
@login_required
def unfollow():
    follow_form = FollowUserForm()
    unfollow_form = UnfollowUserForm()
    clear_form = BlankForm()
    title = 'tweets by keyword'
    if unfollow_form.validate_on_submit():
        followed = Followed.query.filter_by(username=unfollow_form.username_unfollow.data,
                                            follower=current_user).first()
        db.session.delete(followed)
        db.session.commit()
        flash(f'You no longer follow {unfollow_form.username_unfollow.data}')
        return redirect(url_for('main.index'))
    return render_template('index.html', title=title, follow_form=follow_form,
                           unfollow_form=unfollow_form, clear_form=clear_form)


@bp.route('/clear_follow', methods=['POST'])
@login_required
def clear_follow_list():
    form = BlankForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        user.clear_follow_list()
        flash("You've cleared your follow list")
        return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))


@bp.route('/view_followed', methods=['GET'])
@login_required
def view_followed_list():
    user = User.query.filter_by(username=current_user.username).first()
    follow_list = user.get_followed_users()
    return render_template('follow_list.html', follow_list=follow_list)
