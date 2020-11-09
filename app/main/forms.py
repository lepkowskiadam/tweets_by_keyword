from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user


class FollowUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_username(self, username):
        followed = [user.username for user in current_user.followed.all()]
        if username.data in followed:
            raise ValidationError('You already follow this user')

