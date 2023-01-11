
from gpg import Data
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
    username = StringField('ExoLogUsername', validators=[DataRequired(), Length(min=3, max=25)])
    passwd = StringField('ExoLogPassword', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('ExoLogUsername', validators=[DataRequired()])
    passwd = StringField('ExoLogPassword', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember')
    submit = SubmitField('Login')

class NewProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(min=3, max=16)])
    description = StringField('Description', validators=[Length(max=250)])
    submit = SubmitField('Create Project')