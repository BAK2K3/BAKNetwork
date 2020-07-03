######################
###COMMENT FORMS.PY###
######################

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

#Comment Form
class CommentForm(FlaskForm):

    text = TextAreaField('Feel free to add a comment!', validators=[DataRequired(message="Please enter some text to continue!")])
    submit = SubmitField('Submit') 