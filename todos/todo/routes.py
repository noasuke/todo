from flask import Blueprint, render_template, redirect, url_for, request, flash
from todos.models import Todo, Task
from todos.extensions import db, bcrypt
from flask_login import login_required, current_user
from todos.forms import TaskForm
from datetime import date

todo_bp = Blueprint('todo', __name__, template_folder='templates')

@todo_bp.route('/')
def index():
  query = db.select(Task)
  tasks = db.session.scalars(query).all()
  return render_template('todo/todos.html',
                          title='Todos Page',
                          tasks=tasks)

@todo_bp.route('/todos_today', methods=['GET', 'POST'])
@login_required
def todos():
  form = TaskForm()
  # todo = Todo.query.filter(Todo.created_at==date.today(), Todo.user_id==current_user.id).first()
  query = db.select(Todo).where(Todo.created_at==date.today(), Todo.user==current_user)
  todo = db.session.scalar(query)

  if todo:
    # todolist = Task.query.filter(Task.todo_id==todo.id)
    query = db.select(Task).where(Task.todo_id==todo.id)
    tasks = db.session.scalars(query).all()
    if form.validate_on_submit():
      task = form.task.data
      new_task = Task(task_name=task, todo_id=todo.id)
      db.session.add(new_task)
      db.session.commit()

      flash('Add New Task to Task Successfully!',
             'success')
      return redirect(url_for('todo.todos'))
  else:
    tasks = None

  return render_template('todo/todos.html',
                          title='Todos Today', 
                          form=form,
                          todo=todo,
                          tasks=tasks)

@todo_bp.route('/new_todo', methods=['GET', 'POST'])
@login_required
def new_todo():
  created = date.today()
  todo = Todo(created_at=created, user_id=current_user.id)
  db.session.add(todo)
  db.session.commit()

  flash('Create New Todo Successfullt!',
         'success')
  
  return redirect(url_for('todo.todos'))

@todo_bp.route('/<int:id>/task_completed')
@login_required
def task_completed(id):
  task = db.session.get(Task, id)
  task.completed = True
  db.session.commit()

  return redirect(url_for('todo.todos'))

@todo_bp.route('/all_todos')
@login_required
def all_todos():
  tasks = db.session.scalars(db.select(Task).where(Task.todo_id==Todo.id, Todo.user==current_user).order_by(Todo.created_at.desc())).all()
  return render_template('todo/all_todos.html', title='Show All Todos', tasks=tasks)

@todo_bp.route('/completed_todos')
@login_required
def completed_todos():
  tasks = db.session.scalars(db.select(Task).where(Task.todo_id==Todo.id, Todo.user==current_user, Task.completed==True).order_by(Todo.created_at.desc())).all()
  return render_template('todo/all_todos.html',
                         title='Show Completed Tasks',
                         tasks=tasks)

@todo_bp.route('/uncompleted_todos')
@login_required
def uncompleted_todos():
  tasks = db.session.scalars(db.select(Task).where(Task.todo_id==Todo.id, Todo.user==current_user, Task.completed==False).order_by(Todo.created_at.desc())).all()
  return render_template('todo/all_todos.html',
                         title='Show Uncompleted Tasks',
                         tasks=tasks)