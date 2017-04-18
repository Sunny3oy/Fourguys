from flask import Flask
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

bootstrap = Bootstrap(app)
manager = Manager(app)
login_manager = LoginManager()
login_manager.init_app(app)

from app import models, views, forms, managers

