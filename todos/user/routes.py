from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from todos.extensions import db, login_manager, bcrypt
from todos.models import User
from todos.forms import RegisterForm, LoginForm, UpdateUserForm

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/')
@login_required
def index():
  return render_template('user/index.html', title='User Page')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    username = form.username.data
    email = form.email.data
    password = form.password.data
    hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_pwd)
    db.session.add(user)
    db.session.commit()
    flash('Register successful!', 'success')
    return redirect(url_for('user.login'))

  return render_template('user/register.html', 
        title='Register Form', form=form)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    email = form.email.data
    password = form.password.data
    remember = form.remember.data

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
      login_user(user, remember=remember)

      flash('Login Successfull',
             'success')
      return redirect(url_for('user.index'))
    else:
      flash('Login Unsuccessfull. Please check email and password',
             'warning')

  return render_template('user/login.html', 
        title='Login Form', form=form)

@user_bp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('core.index'))

@user_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateUserForm()
  if form.validate_on_submit():
    firstname = form.firstname.data
    lastname = form.lastname.data
    current_user.firstname = firstname
    current_user.lastname = lastname
    db.session.commit()
    flash('Update Account Successfully', 'success')
    return redirect(url_for('user.account'))
  
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname

  return render_template('user/account.html',
                         title='Account Information',
                         form=form)