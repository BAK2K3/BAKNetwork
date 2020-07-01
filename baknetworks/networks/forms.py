##NETWORKS FORMS.PY##

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms import ValidationError

from flask_login import current_user
from baknetworks.models import User

class RNNForm(FlaskForm):

    textrnn = StringField('Input Text', validators=[DataRequired()])
    temprnn = IntegerField(label='Temperature (%)', validators=[DataRequired(), NumberRange(1, 200)])
    submitrnn = SubmitField('Generate') 