from .forms import *
from .models import *
from flask import render_template, flash, url_for, redirect
from flask_login import *

@app.login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

@app.route('/signup',methods=['GET', 'POST'])
def signup1():
    form = signup()
    if form.validate_on_submit():
        if form.password.data != form.conpassword.data:
            flash('Password mush match!')
        else:
            new_user = Customer(username=form.username.data,
                                firstName=form.firstname.data,
                                lastName=form.lastname.data,
                                email=form.email.data,
                                password=form.password.data,
                                address=form.address.data)
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
    return render_template("menu.html", form=form,
                           total=total, number=number, itemdes=itemdes, price=price, iterr=zip(number,itemdes,price),
                           databaseitems = Menu.query.all())

@app.route('/checkout')
def check():

    return render_template("checkout.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = login1()
    if form.validate_on_submit():

        customer = Customer.query.filter_by(username=form.username.data).first()
        if customer:
            if customer.password == form.password.data:
                login_user(customer)
                return redirect(url_for('contact'))
            else:
                flash('Incorrect password or email')
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/checkUser')
def checkUser():
    if current_user.is_authenticated:
        return '<h1> You are logged in, %s %s </h1>' % (current_user.firstName, current_user.lastName)
    else:
        return '<h1> You are logged out </h1>'

@app.route('/contact')
def contact():
    return render_template("contact.html")