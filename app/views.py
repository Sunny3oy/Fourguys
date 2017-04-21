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

@app.route('/',methods=['GET', 'POST'])
def home():
    check = current_user.is_authenticated
    if current_user.is_authenticated:
        return render_template("home.html",user = current_user.firstName,check = check)
    else:
        return render_template("home.html", user = "Guest", check = check)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    form = menu1()
    doge = 0
    sumitem = 0
    if form.validate_on_submit():
        doge = 1
        total = [0,0,0]
        databaseprice1 = FoodItem.query.filter_by(itemID=1).first()
        databaseprice2 = FoodItem.query.filter_by(itemID=2).first()
        databaseprice3 = FoodItem.query.filter_by(itemID=3).first()
        total[0] = databaseprice1.itemPrice * form.qty0.data
        total[1] = databaseprice2.itemPrice * form.qty1.data
        total[2] = databaseprice3.itemPrice * form.qty2.data
        sumitem = sum(total)
        print (total[0],total[1],total[2])
        return render_template("menu.html", form=form, databaseitems=FoodItem.query.all(), doge=doge,total = total,sumitem = sumitem)
    return render_template("menu.html", form=form,databaseitems = FoodItem.query.all(), doge=doge,sumitem = sumitem)

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
                return redirect(url_for('home'))
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

@app.route('/profile')
@login_required
def user_profile():
    return render_template("profile.html", user = current_user)

@app.route('/addmoney', methods=['GET', 'POST'])
@login_required
def addmoney():
    form = accountsetting()
    if form.validate_on_submit():
        current_user.acctBal = form.addmoney.data + current_user.acctBal
        db.session.commit()
        return render_template("addmoney.html",form = form, user = current_user)
    return render_template("addmoney.html",form = form, user = current_user)