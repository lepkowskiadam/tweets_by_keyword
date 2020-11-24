from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user


class FollowUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    follow_submit = SubmitField('Follow')

    def validate_username(self, username):
        followed = [user.username for user in current_user.followed.all()]
        if username.data in followed:
            raise ValidationError('You already follow this user')


class UnfollowUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    unfollow_submit = SubmitField('Unfollow')

    def validate_username(self, username):
        followed = [user.username for user in current_user.followed.all()]
        if username.data not in followed:
            raise ValidationError('User not found in followed list')