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

@app.route('/',methods=['GET', 'POST'])
def home():
    check = current_user.is_authenticated
    if current_user.is_authenticated:
        return render_template("home.html",user = current_user.firstName,check = check)
    else:
        return render_template("home.html", user = "Guest", check = check)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    doge = 0                  #0 if no shopping cart, 1 otherwise
    sumitem = 0               #Saves total sum of food items
    numbers = [0, 1, 2, 3, 4] #Used to render 'rating hearts'
    validate = True           #Used to validate ALL forms, if at least one is not validated it becomes false.

    #Place Order and Shopping Cart Buttons
    placebutton = PlaceButton(prefix="myplaceorder")
    shopbutton = ShopButton(prefix="myshopcart")


    #List that will hold n forms, where n is the size of the FoodItems table
    n = 16 #for now fixed n (Need 'n' to be the size of the FoodItems table)
    formlist = []

    #The following loop creates a list of forms.
    for i in range(0,n):
        ithform = menu1(prefix="form" + str(i)) #Create the ith form with unique prefix
        formlist.append(ithform)                #Append to form list

    #Validate all forms
    for i in formlist:
        validate = validate and i.validate_on_submit()

    if validate and shopbutton.submit.data:

        doge = 1    #Shopping Cart should be displayed

        #The following gets the prices for all food items from db
        itemPrices = []
        for i in range(1,n+1):
            itemPrices.append(FoodItem.query.filter_by(itemID=i).first().itemPrice)

        #Dictonary of subtotals for each item.
        subtotals = []
        for i in range(0,n):
            item_subtotal = itemPrices[i] * formlist[i].qty.data
            subtotals.append(item_subtotal)

        sumitem = sum(subtotals)    #Get total

        # Create a key-value pair in the session dictionary to store the total
        session['ProductTotal'] = sum(subtotals)
        # This key-value pair ensures that when the checkout page is refreshed,
        # the customer is not charged more than once
        session['orderMade'] = False

        return render_template("menu.html", formlist=formlist, databaseitems=FoodItem.query.all(), doge=doge,total = subtotals,sumitem = sumitem,shopbutton=shopbutton, placebutton=placebutton,numbers=numbers)

    elif placebutton.submit.data:
        return checkout()

    return render_template("menu.html", formlist=formlist, databaseitems=FoodItem.query.all(), doge=doge, sumitem=sumitem,shopbutton=shopbutton, placebutton=placebutton,numbers=numbers)

@app.route('/checkout')
@login_required
def checkout():
    # Get the value stored in the session['ProductTotal'] and store it in cartTotal
    # If there is no item on the cart, return a message for them to return to menu
    # Otherwise, process the order.

    # If the checkout menu is refreshed, the user will be redirected to menu page
    diffmessg = None
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