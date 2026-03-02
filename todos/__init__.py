from flask import Flask
from todos.extensions import db, login_manager, bcrypt
import os
from todos.core.routes import core_bp
from todos.user.routes import user_bp
from todos.todo.routes import todo_bp

from todos.models import User, Todo, Task

def create_app():
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
  
  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)

  login_manager.init_app(app)
  login_manager.login_view = 'login'
  login_manager.login_message_category = 'info'

  app.register_blueprint(core_bp, url_prefix='/')
  app.register_blueprint(user_bp, url_prefix='/users')
  app.register_blueprint(todo_bp, url_prefix='/todos')

  return app


