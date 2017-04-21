from .forms import *
from .models import *
from flask import render_template, flash, url_for, redirect, session
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
    # button = buttonform()
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
        #return render_template("menu.html", form=form, databaseitems=FoodItem.query.all(), doge=doge,total = total,sumitem = sumitem)

        # Create a key-value pair in the session dictionary to store the total
        session['ProductTotal'] = sum(total)
        # This key-value pair ensures that when the checkout page is refreshed,
        # the customer is not charged more than once
        session['orderMade'] = False
        if current_user.is_authenticated:
            return redirect(url_for('checkout'))
        else:
            return '<p> Hold on!!! You need to login first</p>'
    # elif button.validate_one_submit():
    #     return check(sumitem)
    return render_template("menu.html", form=form,databaseitems = FoodItem.query.all(), doge=doge,sumitem = sumitem)

@app.route('/checkout')
@login_required
def checkout():
    # Get the value stored in the session['ProductTotal'] and store it in cartTotal
    # If there is no item on the cart, return a message for them to return to menu
    # Otherwise, process the order.

    # If the checkout menu is refreshed, the user will be redirected to menu page
    cartTotal = session.get('ProductTotal')

    if cartTotal == 0:
        return '<p>You have not selected anything, go back to <a href="menu">menu</a>!!!<p>'
    else:
        difference = cartTotal - current_user.acctBal
        if session.get('orderMade'):
            return redirect(url_for('menu'))
        else:
            if cartTotal > current_user.acctBal:
                message = 'Seems like you need a new job.'
            else:
                message = 'Good to go!'
                diffmessg = "Difference " + str(current_user.acctBal) + " - " + str(cartTotal) + " = " + str(difference)
                current_user.acctBal = current_user.acctBal - cartTotal
                db.session.add(current_user)
                db.session.commit()
                session['orderMade'] = True
    return render_template("checkout.html", total=cartTotal, newbalance=current_user.acctBal, message=message, diffmessg=diffmessg)

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