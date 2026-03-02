from todos.extensions import db, login_manager
from datetime import date
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey, Boolean, func
from typing import List

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  username: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)
  email: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
  firstname: Mapped[str] = mapped_column(String(30), nullable=True)
  lastname: Mapped[str] = mapped_column(String(30), nullable=True)
  password: Mapped[str] = mapped_column(String(100), nullable=False)

  todos: Mapped[List['Todo']] = relationship(back_populates='user')

  def __repr__(self):
    return f'<User: {self.username}>'
  
class Todo(db.Model):
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  created_at: Mapped[date] = mapped_column(Date(), default=date.today())
  user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))

  tasks: Mapped[List['Task']] = relationship(back_populates='todo')
  user: Mapped[User] = relationship(back_populates='todos')

  def __repr__(self):
    return f'<Todo: {self.created_at}>'
  
class Task(db.Model):
  id: Mapped[int] = mapped_column(Integer, primary_key=True)
  task_name: Mapped[str] = mapped_column(String(100), nullable=False)
  completed: Mapped[bool] = mapped_column(Boolean, default=False)
  todo_id: Mapped[int] = mapped_column(Integer, ForeignKey(Todo.id))

  todo: Mapped[Todo] = relationship(back_populates='tasks')

  def __repr__(self):
    return f'<Task: {self.task_name}>'