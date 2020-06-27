###COMMENT FORMS.PY###

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms import ValidationError

from flask_login import current_user
from baknetworks.models import User

class CommentForm(FlaskForm):

    text = TextAreaField('Feel free to add a comment!', validators=[DataRequired(message="Please enter some text to continue!")])
    submit = SubmitField('Submit') 