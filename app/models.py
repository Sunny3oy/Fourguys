from app import app
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(15))
    lastname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    address = db.Column(db.String(50))
    card = db.Column(db.String(50))

class items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemname= db.Column(db.String(15), unique=True)
    price = db.Column(db.Integer)
    chef = db.Column(db.String(15))
    itemdes = db.Column(db.String(50))