from flask import Flask
from flask_bootstrap import Bootstrap
from flask_script import Manager

app = Flask(__name__)
app.config.from_object('config')

bootstrap = Bootstrap(app)
manager = Manager(app)

from app import models, views, forms, managers

