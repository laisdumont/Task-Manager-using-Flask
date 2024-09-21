from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from logging.handlers import SysLogHandler
from dotenv import load_dotenv
import logging
import os


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

syslog = SysLogHandler(address='/dev/log')
syslog.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)s %(process)d[pid]: %(message)s')
syslog.setFormatter(formatter)
app.logger.addHandler(syslog)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'danger'

bcrypt = Bcrypt(app)

# Always put Routes at end
from todo_project import routes