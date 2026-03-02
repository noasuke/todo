from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from todos.models import User

class RegisterForm(FlaskForm):
  username = StringField('Username', 
      validators=[DataRequired(), Length(min=4, max=20)])
  email = EmailField('Email Address', 
      validators=[DataRequired(), Email()])
  password = PasswordField('Password', 
      validators=[DataRequired()])
  confirm_password = PasswordField('Confirm Password', 
      validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is taken. Please choose different one!')
    
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError('That email is taken. Please choose different one!')
  

class LoginForm(FlaskForm):
  email = EmailField('Email Address', 
      validators=[DataRequired(), Email()])
  password = PasswordField('Password', 
      validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')
  

class TaskForm(FlaskForm):
  task = StringField('Task', validators=[DataRequired(), 
                        Length(min=5, max=50)],
                        render_kw={'placeholder':'enter your task'})
  submit = SubmitField('Add New Task')

class UpdateUserForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)],
                          render_kw={'readonly':'readonly'})
  email = EmailField('Email Address', validators=[DataRequired(), Email()], 
                     render_kw={'readonly':'readonly'})
  firstname = StringField('Firstname')
  lastname = StringField('Lastname')
  
  submit = SubmitField('Update User Info')