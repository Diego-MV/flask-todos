from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired #estudiar validators

class Login_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Signup_Form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


