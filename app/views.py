from functools import wraps

from .forms import *
from .models import *
from flask import render_template, flash, url_for, redirect, session, current_app
from flask_login import *


# override the built-in login_required() function
def login_required(role='ANY'):
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            user_role = current_user.get_user_type()
            if (user_role != role) and (role != 'ANY'):
                return current_app.login_manager.unauthorized()
            return f(*args, **kwargs)
        return decorated_view
    return wrapper


# @app.login_manager.user_loader
# def load_user(user_id):
#     print(user_id)
#     return Customer.query.get(int(user_id))

@app.login_manager.user_loader
def load_user(user_id):
    print(user_id)
    if int(user_id) > 1000: #Only employees have ID's > 1000
        return Employee.query.get(int(user_id))
    else:
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
    #typeofUser=""
    if check:
        typeofUser = current_user.get_user_type()
        if typeofUser == "CUSTOMER":
            numberType = 0
        elif typeofUser == "MANAGER":
            numberType = 1
        elif typeofUser == "CHEF":
            numberType = 2
        else:
            numberType = 3  # Deliver

    if current_user.is_authenticated:
        return render_template("home.html",user = current_user.firstName,check = check,numberType=numberType)
    else:
        return render_template("home.html", user = "Guest", check = check)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    doge = 0                  #0 if no shopping cart, 1 otherwise
    sumitem = 0               #Saves total sum of food items
    numbers = [0, 1, 2, 3, 4] #Used to render 'rating hearts'
    validate = True           #Used to validate ALL forms, if at least one is not validated it becomes false.

    #This function inputs the items of a menu and a keyword.
    #Creates the number of forms neccesary for the specific menu list using the keyword.
    def make_forms_for_items(listOfItems,keyword):
        formlist = []
        for i in range (0,len(listOfItems)):
          form = menu1(prefix=str(keyword)+str(i))  #Create a unique form with the keyword for each menu item
          formlist.append(form)
        return formlist

    #Get menus names, menu descriptions,list of menu items and forms forms for menu belonging to that menu
    #To do this we will form triplets (menuName,menuDesc,listOfMenuItems,forms)
    menus = []

    for i in range (1,get_table_size(Menu) + 1):
        menuName = Menu.query.filter_by(menuID=i).first().menuName
        menuDesc = Menu.query.filter_by(menuID=i).first().menuDesc
        menuID = Menu.query.filter_by(menuID=i).first().menuID
        listOfMenuItems = get_all_food_items_by_menu(menuID)
        formlist = make_forms_for_items(listOfMenuItems,i)

        #Append to menus[]
        menus.append((menuName,menuDesc,listOfMenuItems,formlist))

    #print(menus)

    #Place Order and Shopping Cart Buttons
    placebutton = PlaceButton(prefix="myplaceorder")
    shopbutton = ShopButton(prefix="myshopcart")

    #Validate all forms
    for i in range(0,len(menus)):
        for j in range (0,len(menus[i][3])):
            validate = validate and menus[i][3][j].validate_on_submit()

    if validate and shopbutton.submit.data:

        doge = 1    #Shopping Cart should be displayed

        #Gets names and prices for each of the menu items in all menus
        foodnames = []
        itemPrices = []
        for menu in menus:
            for fooditem in menu[2]:
                foodnames.append(fooditem.itemName)
                itemPrices.append(fooditem.itemPrice)

        #Gets the quantity for each form the user inputs
        formsInput =[]
        for menu in menus:
            for thisform in menu[3]:
                formsInput.append(thisform.qty.data)

        #Get subtotals
        subtotals = []
        for i in range(0, len(itemPrices)):
            item_subtotal = itemPrices[i] * formsInput[i]
            subtotals.append(item_subtotal)

        sumitem = sum(subtotals)    #Get total

        # Create a key-value pair in the session dictionary to store the total
        session['ProductTotal'] = sum(subtotals)
        # This key-value pair ensures that when the checkout page is refreshed,
        # the customer is not charged more than once
        session['orderMade'] = False

        return render_template("menu.html",databaseitems=menus,foodnames= foodnames,itemPrices=itemPrices,formsInput=formsInput, doge=doge,total = subtotals,sumitem = sumitem,shopbutton=shopbutton, placebutton=placebutton,numbers=numbers)

    elif placebutton.submit.data:
        return checkout()

    return render_template("menu.html",  databaseitems=menus, doge=doge, sumitem=sumitem,shopbutton=shopbutton, placebutton=placebutton,numbers=numbers)

@app.route('/checkout')
@login_required('CUSTOMER')
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

@app.route('/loginEmployee', methods=['GET', 'POST'])
def login_employee():
    loginForm = loginEmployee()
    if loginForm.validate_on_submit():
        employee = Employee.query.filter_by(username=loginForm.employee.data).first()
        if employee:
            if employee.password == loginForm.password.data:
                login_user(employee)
                print("EMPLY LOGGED IN")
                return redirect(url_for('home'))
            else:
                flash('Incorrect password or email')
    return render_template("loginEmployee.html",loginForm=loginForm)

@app.route('/logout')
@login_required()
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/checkUser')
def checkUser():
    if current_user.is_authenticated:
        return '<h1> You are logged in, %s %s </h1>' % (current_user.firstName, current_user.lastName,current_user.get_user_type())
    else:
        return '<h1> You are logged out </h1>'

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/profile')
@login_required('CUSTOMER')
def user_profile():
    return render_template("profile.html", user = current_user)

@app.route('/managerPage',methods=['GET', 'POST'])
@login_required('MANAGER')
def manager_page():

    managerForm = managerButtons(prefix="Manager Buttons") #Creates buttons for manager functionalities

    #***THE FOLLOWING IS TO GET THE DYNAMIC DROPLISTS FOR EMPLYEES AND CUSTOMERS***#
    ###Getting employee drop list###
    employeeList = []
    employees = get_employees()
    for employee in employees:
        if not employee.emplType == 0:  # Managers (type 0) are not subject to promotions or demotions
            if employee.emplType == 1:
                employeeType = "Chef: "
            else:
                employeeType = "Delv: "
            employeeList.append((employee.id, employeeType + employee.firstName + ' ' + employee.lastName))
    managerForm.employeeDropList.choices = employeeList
    ###Getting customers drop list###
    customersList = []
    customers = get_customers()
    for customer in customers:
        # Do not forget to put a condition here that checks whether they are MVP or NOT
        customersList.append((customer.id, customer.firstName + ' ' + customer.lastName))
    managerForm.customerDropList.choices = customersList
    ################################

    if managerForm.hire.data:
        return redirect(url_for('hire'))
    elif managerForm.fire.data:
        return 1
    elif managerForm.promoteE.data:
        return 1
    elif managerForm.demoteE.data:
        return 1
    elif managerForm.promoteE.data:
        return 1
    elif managerForm.demoteE.data:
        return 1

    return render_template("managerPage.html",managerForm=managerForm)

@app.route('/hire',methods=['GET', 'POST'])
@login_required('MANAGER')
def hire():
    hireform = hireEmployee()

    #When chefs are created they also need an empty default menu

    if hireform.submit.data:
        if hireform.password.data != hireform.conpassword.data:
            flash('Passwords must match dumb manager!')
        else:
            new_employee = Employee(username = hireform.username.data,
                                    firstName = hireform.firstname.data,
                                    lastName = hireform.lastname.data,
                                    emplType= int(hireform.typeDropList.data),
                                    numComplaint = 0,
                                    payGrade = int(hireform.salaryDropList.data),
                                    password = hireform.password.data)
            db.session.add(new_employee)
            db.session.commit()
            print("Type plus sal:" + hireform.typeDropList.data + ' ' + hireform.salaryDropList.data)

            #Create menu if it is a chef
            if int(hireform.typeDropList.data) == 1: #Create empty menu for chef
                new_menu = Menu(chefID = new_employee.id,
                                menuName = "To Name",
                                menuDesc = "To Write Description")
                db.session.add(new_menu)
                db.session.commit()
                print("MENU CREATED!")
            return redirect(url_for('manager_page'))



    # form = signup()
    # if form.validate_on_submit():
    #     if form.password.data != form.conpassword.data:
    #         flash('Password mush match!')
    #     else:
    #         new_user = Customer(username=form.username.data,
    #                             firstName=form.firstname.data,
    #                             lastName=form.lastname.data,
    #                             email=form.email.data,
    #                             password=form.password.data,
    #                             address=form.address.data)
    #         db.session.add(new_user)
    #         db.session.commit()
    #         return redirect(url_for('login'))

    return render_template("hire.html",hireForm=hireform)

@app.route('/chefPage',methods=['GET', 'POST'])
@login_required('CHEF')
def chef_Page():

    addToTheMenu = addToMenu(prefix="Add")
    removeFromMenu = deleteFromMenu(prefix="Delete")

    #We need to know which chef is cureently logged in to determine the menu or menus that he/she posseses
    listOfMenuItems = get_all_food_items_by_chef(current_user.id)

    menuForChef = get_all_menus_by_chef(current_user.id)
    menuID = int(menuForChef[0].menuID)

    if addToTheMenu.submit.data:

        newItem = addToTheMenu.droplist.data

        print(menuForChef) #Prints the chef menus in a list
        print(newItem)#prints Food Item ID
        print(menuForChef[0].menuID,"::::MENU ID FOR CHEF")

        #Get size of current MenuItems table
        nextMenuID = get_table_size(MenuItem)
        print("BEFORE ",nextMenuID)

        if not is_food_item_exist(menuID,newItem):
            new_menu_item = MenuItem(menuItemID = nextMenuID,
                                    menuID = menuID,
                                    itemID = newItem ,
                                    menuItemRating= 5)
            db.session.add(new_menu_item)
            db.session.commit()

        print("AFTER:",get_table_size(MenuItem))

        #listOfMenuItems = get_all_food_items_by_menu(1)  # Fixed to menu1
        listOfMenuItems = get_all_food_items_by_chef(current_user.id)

        return render_template("chefPage.html", add=addToTheMenu,delete = removeFromMenu,  menu=listOfMenuItems)

    elif removeFromMenu.submit.data:

        print("BEFORE DELETE:", get_table_size(MenuItem))

        MenuItem.query.filter_by(itemID=removeFromMenu.droplist.data,menuID=menuID).delete() #Make only one be removed
        db.session.commit()
        listOfMenuItems = get_all_food_items_by_chef(current_user.id)
        print("AFTER DELETE:", get_table_size(MenuItem))
        return render_template("chefPage.html", add=addToTheMenu,delete = removeFromMenu, menu=listOfMenuItems)

    return render_template("chefPage.html" ,add = addToTheMenu,delete = removeFromMenu, menu = listOfMenuItems)

@app.route('/deliverPage',methods=['GET', 'POST'])
@login_required('DELIVERY')
def deliver_Page():
    return render_template("deliverPage.html")

@app.route('/addmoney', methods=['GET', 'POST'])
@login_required('CUSTOMER')
def addmoney():
    form = accountsetting()
    if form.validate_on_submit():
        current_user.acctBal = form.addmoney.data + current_user.acctBal
        db.session.commit()
        return render_template("addmoney.html",form = form, user = current_user)
    return render_template("addmoney.html",form = form, user = current_user)

@app.route('/argh', methods=['GET'])
@login_required('CUSTOMER')
def argh():
    return "You are either not logged in as a customer or not logged in at all"