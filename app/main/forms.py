from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user
from twitter_handler import TwitterHandler


class FollowUserForm(FlaskForm):
    username_follow = StringField('Follow', validators=[DataRequired()])
    follow_submit = SubmitField('Follow')

    def validate_username_follow(self, username):
        followed = [user.username for user in current_user.followed.all()]
        if username.data in followed:
            raise ValidationError('You already follow this user')
        elif not TwitterHandler.verify_user_exists(username.data):
            raise ValidationError(f'No user named <{username.data}> found on twitter')


class UnfollowUserForm(FlaskForm):
    username_unfollow = StringField('Unfollow', validators=[DataRequired()])
    unfollow_submit = SubmitField('Unfollow')

    def validate_username_unfollow(self, username):
        followed = [user.username for user in current_user.followed.all()]
        if username.data not in followed:
            raise ValidationError('User not found in followed list')


class BlankForm(FlaskForm):
    submit = SubmitField('Submit')
