from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email


class RegistrationForm(FlaskForm): name = StringField('Full Name', validators=[DataRequired()])


email = StringField('Email', validators=[DataRequired(), Email()])
password = PasswordField('Password', validators=[DataRequired()])
submit = SubmitField('Register')


class LoginForm(FlaskForm): email_or_username = StringField('Email or Username', validators=[DataRequired()])


password = PasswordField('Password', validators=[DataRequired()])
submit = SubmitField('Login')


class UpdateProfileForm(FlaskForm): name = StringField('Full Name', validators=[DataRequired()])


email = StringField('Email', validators=[DataRequired(), Email()])
password = PasswordField('Enter Password to Confirm Changes', validators=[DataRequired()])
submit = SubmitField('Save Changes')


class UpvoteForm(FlaskForm): submit = SubmitField()
