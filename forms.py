from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField, RadioField, Label, TextField, PasswordField, SubmitField
from wtforms.widgets.core import TextArea
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    login = TextField('Username', validators=[DataRequired()], render_kw={"placeholder": "username"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "password"})
    submit = SubmitField('Submit')