##NETWORKS FORMS.PY##

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, IntegerField 
from wtforms.validators import DataRequired, NumberRange
from wtforms import ValidationError

from flask_login import current_user
from baknetworks.models import User

#Form for RNN Pages
class RNNForm(FlaskForm):

    textrnn = StringField('Input Text', validators=[DataRequired()])
    temprnn = IntegerField(label='Temp (%)', validators=[DataRequired(), NumberRange(1, 200)])
    submitrnn = SubmitField('Generate') 

#Form for CNN Pages
class CNNForm(FlaskForm):

    filecnn = FileField('Select File', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submitcnn = SubmitField('Submit')