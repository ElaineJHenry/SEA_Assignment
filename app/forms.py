from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max = 64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min = 8)])
    passwordCheck = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Admin', 'Admin'), ('User', 'User')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Username is already in use. Please use another.')
        
class AuthorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max = 64)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=150)])
    submit = SubmitField('Submit')

class BookForm(FlaskForm):
    author = SelectField('Author', validators=[DataRequired()], choices=[])
    name = StringField('Name', validators=[DataRequired(), Length(max = 64)])
    release = DateField('Release Date', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired(), Length(max = 64)])
    pages = IntegerField('Pages', validators=[DataRequired(), NumberRange(min=0, max=9999)])
    submit = SubmitField('Submit')