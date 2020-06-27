##NETWORKS FORMS.PY##

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms import ValidationError

from flask_login import current_user
from baknetworks.models import User

class RNNForm(FlaskForm):

    textrnn = StringField('Input Text', validators=[DataRequired()])
    submitrnn = SubmitField('Generate') 