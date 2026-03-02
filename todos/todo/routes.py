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
  todo = Todo.query.filter(Todo.created_at==date.today(), Todo.user_id==current_user.id).first()
  
  if todo:
    todolist = Task.query.filter(Task.todo_id==todo.id)
    if form.validate_on_submit():
      task = form.task.data
      todolist = Task(task_name=task, todo_id=todo.id)
      db.session.add(todolist)
      db.session.commit()

      flash('Add New Task to Task Successfully!',
             'success')
      return redirect(url_for('todo.todos'))
  else:
    todolist = None

  return render_template('todo/todos.html',
                          title='Todos Today', 
                          form=form,
                          todo=todo,
                          todolist=todolist)

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