from flask_wtf import FlaskForm
from wine.wine.models import User
from wtforms import IntegerField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, ValidationError


class SearchFrom(FlaskForm):
    winery = StringField('Winery', validators=[Length(max=20)])
    country = StringField('Country', validators=[Length(max=20)])
    title = StringField('Wine Name', validators=[Length(max=20)])
    points = StringField('Points', validators=[Length(max=20)])
    variety = StringField('Variety', validators=[Length(max=20)])
    submit = SubmitField('Search')

    class Meta:
        csrf = False


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken')
    
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email address is already in use')


class LoginForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class WineForm(FlaskForm):
    title = StringField('Wine Name', 
        validators=[DataRequired(), Length(min=2, max=50)])
    winery = StringField('Winery', 
        validators=[DataRequired(), Length(min=2, max=20)])
    country = StringField('Country', 
        validators=[DataRequired(), Length(min=2, max=20)])
    province = StringField('Province', 
        validators=[Length(max=20)])
    variety = StringField('Variety', 
        validators=[Length(max=40)])
    points = IntegerField('Rating', 
        validators=[DataRequired(), NumberRange(min=0, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('Submit')

    class Meta:
        csrf = False


class ResetPasswordForm(FlaskForm):
    username = StringField('Username', 
        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')


class CommentForm(FlaskForm):
    content = TextAreaField('Add a comment', validators=[Length(max=120)])
    submit = SubmitField('Post')


class FavoriteForm(FlaskForm):
    clicked = SubmitField('Submit')
