__author__ = 'drole'

from flask.ext.login import LoginManager
from flask import Flask

lm = LoginManager()
app = Flask(__name__)
app.config.from_object('config')
from app import views
