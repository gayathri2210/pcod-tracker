# project/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

# Import the User model for validation purposes.
# This import should be fine as long as models.py doesn't import from forms.py.
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), 
                                       Length(min=2, max=20, message="Username must be between 2 and 20 characters.")])
    email = StringField('Email',
                        validators=[DataRequired(), 
                                    Email(message="Invalid email address.")])
    password = PasswordField('Password', 
                             validators=[DataRequired(), 
                                         Length(min=6, message="Password must be at least 6 characters long.")])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), 
                                                 EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Sign Up')

    # Custom validator to check if the username is already taken
    def validate_username(self, username_field):
        user = User.query.filter_by(username=username_field.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

    # Custom validator to check if the email is already registered
    def validate_email(self, email_field):
        user = User.query.filter_by(email=email_field.data.lower()).first() # Check lowercase email
        if user:
            raise ValidationError('That email address is already registered. Please choose a different one or login.')


class LoginForm(FlaskForm):
    # This field can accept either an email or a username
    email_or_username = StringField('Email or Username', 
                                    validators=[DataRequired()])
    password = PasswordField('Password', 
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me') # For "Remember Me" functionality
    submit = SubmitField('Login')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', 
                                     validators=[DataRequired()])
    new_password = PasswordField('New Password', 
                                 validators=[DataRequired(), 
                                             Length(min=6, message="New password must be at least 6 characters long.")])
    confirm_new_password = PasswordField('Confirm New Password',
                                         validators=[DataRequired(), 
                                                     EqualTo('new_password', message="New passwords must match.")])
    submit = SubmitField('Change Password')

