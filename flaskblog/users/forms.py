from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	username = StringField('Username'
		,[DataRequired(), Length(min=6,max=20)])
	email = StringField('Email'
		,[DataRequired(), Email()])
	password = PasswordField('Password'
		,[DataRequired()])
	confirm_password = PasswordField('Confirm Password'
		,[DataRequired(),EqualTo('password')])
	# validate username, email prior to submit
	def validate_username(self,username):
		user = User.query.filter_by(username = username.data).first() # return [] if none
		if user:
			raise ValidationError('Username is taken. Choose a different username')
		pass

	def validate_email(self,email):
		user = User.query.filter_by(email = email.data).first() # return [] if none
		if user:
			raise ValidationError('Email is taken. Choose a different email')
		pass

	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email'
		,[DataRequired(), Email()])
	password = PasswordField('Password'
		,[DataRequired()])
	remember = BooleanField('Remember Me')

	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username'
		,[DataRequired(), Length(min=6,max=20)])
	email = StringField('Email'
		,[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg','png'])])

	submit = SubmitField('Update')

	# validate username, email prior to submit
	def validate_username(self,username):
		if username.data != current_user.username:
			user = User.query.filter_by(username = username.data).first()
			if user:
				raise ValidationError('Username is taken. Choose a different username')
		pass

	def validate_email(self,email):
		if email.data != current_user.email:
			user = User.query.filter_by(email = email.data).first() # return [] if none
			if user:
				raise ValidationError('Email is taken. Choose a different email')
		pass

class RequestResetForm(FlaskForm):
	email = StringField('Email'
		,[DataRequired(), Email()])
	submit= SubmitField('Request Password Reset')

	def validate_email(self,email):
		user = User.query.filter_by(email = email.data).first() # return [] if none
		if user is None:
			raise ValidationError('No account with this email. Pls register first')
		pass

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password'
		,[DataRequired()])
	confirm_password = PasswordField('Confirm Password'
		,[DataRequired(),EqualTo('password')])

	submit= SubmitField('Reset Password')