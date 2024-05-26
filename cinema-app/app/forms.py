from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class PastebinEntry(FlaskForm):
    marks = SelectField(
        'Выберите оценку', 
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )
    submit = SubmitField('Оценить')