import os
from flask import Flask, render_template, flash,url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy

# For paths to files relative to this script.
basedir = os.path.abspath( os.path.dirname(__file__) )

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'key'
Bootstrap(app)

# os.path.join is used to say 'basedir/database.db' without worrying if
# this will be run on a UNIX or Windows system.
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
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
#forms
class signup(FlaskForm):
    firstname = StringField('First name', validators=[InputRequired()])
    lastname = StringField('Last name', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    conpassword = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80), ])
    address = StringField('Address', validators=[InputRequired()])
    card = PasswordField('Card Number', validators=[InputRequired()])

class login1(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class menu1(FlaskForm):
    qty = IntegerField('qty', validators=[InputRequired()], default=0)

@app.route('/signup',methods=['GET', 'POST'])
def signup1():
    form = signup()
    if form.validate_on_submit():
        if form.password.data != form.conpassword.data:
            flash('Password mush match!')
        else:
            new_user = user(firstname=form.firstname.data,
                            lastname=form.lastname.data,
                            email=form.email.data,
                            password=form.password.data,
                            address = form.address.data,
                            card=form.card.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template("Signup.html", form=form)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    form = menu1()
    number = [
        '1.Cheeseburger','2.Rice','3.Doge','4.Indo Coca Cola','5.Waifu'
    ]
    itemdes = [
        'Cheap Ass Burger', 'If you are Asian, get this', 'Animal abuse? Call PETA!', 'Limited time Coca Cola from Indo!',
        'Nier Automata 2B'
    ]
    price = [
        1.00,2.00, 100.00, 3.00, 500.00
    ]
    total = [0]

    if form.validate_on_submit():

        return render_template("checkout.html", total=total)
    return render_template("menu.html",form=form,
                           total=total,number=number, itemdes=itemdes, price=price, iterr=zip(number,itemdes,price),
                           databaseitems = items.query.all())

@app.route('/checkout')
def check():

    return render_template("checkout.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = login1()
    if form.validate_on_submit():

        User = user.query.filter_by(email = form.email.data).first()
        if User:
            if User.password == form.password.data:
                return redirect(url_for('contact'))
            else:
                flash('Incorrect password or email')
    return render_template("login.html", form=form)

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run()
