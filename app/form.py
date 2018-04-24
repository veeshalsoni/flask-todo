from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo
from datetime import datetime

class LoginForm(FlaskForm):
	email = StringField('Email', validators = [DataRequired(),Email()])
	password = PasswordField('Password',validators = [DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField("Sign In")

class SignUpForm(FlaskForm):
	username = StringField('Name', validators = [DataRequired()])
	email = StringField('Email', validators = [DataRequired(),Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	repassword = PasswordField('Re-Type Password', validators = [DataRequired(),EqualTo('password')])
	submit = SubmitField("Sign Up")

class TaskForm(FlaskForm):
	taskdate = DateField('Date', format="%Y-%m-%d", validators = [DataRequired()], default = datetime.today())
	text = TextAreaField('Task', validators = [DataRequired()])
	category = StringField('Category')
	submit = SubmitField('Add')

class DatePostsForm(FlaskForm):
	date = DateField('Date', format="%Y-%m-%d", validators = [DataRequired()], default = datetime.today())
	submit = SubmitField('Show')
