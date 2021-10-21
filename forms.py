from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField, RadioField, Label, TextField, PasswordField, SubmitField
from wtforms.widgets.core import TextArea

class LoginForm(FlaskForm):
    login = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')



class GameForm(FlaskForm):