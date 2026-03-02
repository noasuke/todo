from todos import db, app, bcrypt
from flask import render_template, redirect, url_for, flash, request
from todos.forms import RegisterForm, LoginForm, TaskForm, UpdateUserForm
from todos.models import User, Todo, TodoList
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date

@app.route('/')
def index():
  return render_template('index.html', title='Todo Home Page')

@app.route('/user/register', methods=['GET', 'POST'])
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

    return redirect(url_for('login'))

  return render_template('user/register.html', 
        title='Register Form', form=form)

@app.route('/user/login', methods=['GET', 'POST'])
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
      return redirect(url_for('index'))
    else:
      flash('Login Unsuccessfull. Please check email and password',
             'danger')

  return render_template('user/login.html', 
        title='Login Form', form=form)

@app.route('/user/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/user/account', methods=['GET', 'POST'])
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
    return redirect(url_for('account'))
  
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname

  return render_template('user/account.html',
                         title='Account Information',
                         form=form)

@app.route('/todos/todos_today', methods=['GET', 'POST'])
@login_required
def todos():
  form = TaskForm()
  todo = Todo.query.filter(Todo.created==date.today(), Todo.user_id==current_user.id).first()
  
  if todo:
    todolist = TodoList.query.filter(TodoList.todo_id==todo.id)
    if form.validate_on_submit():
      task = form.task.data
      todolist = TodoList(task=task, todo_id=todo.id)
      db.session.add(todolist)
      db.session.commit()

      flash('Add New Task to Todolist Successfully!',
             'success')
      return redirect(url_for('todos'))
  else:
    todolist = None

  return render_template('todo/todos.html',
                          title='Todos Today', 
                          form=form,
                          todo=todo,
                          todolist=todolist)

@app.route('/todos/new_todo', methods=['GET', 'POST'])
@login_required
def new_todo():
  created = date.today()
  todo = Todo(created=created, user_id=current_user.id)
  db.session.add(todo)
  db.session.commit()

  flash('Create New Todo Successfullt!',
         'success')
  
  return redirect(url_for('todos'))

@app.route('/todos/<int:id>/task_completed')
@login_required
def task_completed(id):
  task = TodoList.query.get(id)
  task.completed = True
  db.session.commit()

  return redirect(url_for('todos'))

