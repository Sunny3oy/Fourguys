from functools import wraps
#Office: We's NAC 8/209
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


@app.route('/signup', methods=['GET', 'POST'])
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
    numberType = 4 #For guests
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

    topFoods = []
    if numberType == 0: #Customer Top Five Items
        topFoods = get_top_five_items(current_user.username)
    else:
        topFoods = FoodItem.query \
        .filter(FoodItem.itemRating == 5) \
        .limit(5).all()

    #Write a sytax checker for the little schemer(EXAM!)
    #What is about this interpreter that supports first class functions, and lexical scoping
    #Used of the slide show
    fooditems = get_all_food_items()
    foodPics = []
    foodNames = []
    for food in fooditems:
        foodPics.append(food.itemPict)
        foodNames.append(food.itemName)
    lenPics = len(foodPics)


    if current_user.is_authenticated:
        return render_template("newHome.html",user = current_user.firstName,check = check,numberType=numberType,topFoods=topFoods,foodPics=foodPics,lenPics=lenPics,foodNames=foodNames)
    else:
        return render_template("newHome.html", user = "Guest", check = check,topFoods=topFoods,foodPics=foodPics,lenPics=lenPics,foodNames=foodNames)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    check = current_user.is_authenticated
    # typeofUser=""
    numberType=5 #Guest
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
        if Menu.query.filter_by(menuID=i).first().activated == True:
            menuName = Menu.query.filter_by(menuID=i).first().menuName
            menuDesc = Menu.query.filter_by(menuID=i).first().menuDesc
            menuID = Menu.query.filter_by(menuID=i).first().menuID
            listOfMenuItems = get_all_food_items_by_menu(menuID)
            formlist = make_forms_for_items(listOfMenuItems,i)

            #Append to menus[]
            menus.append((menuName, menuDesc, listOfMenuItems, formlist,menuID))

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
        foodIds = []
        menuIDs = []
        for menu in menus:
            for fooditem in menu[2]:
                foodnames.append(fooditem.itemName)
                itemPrices.append(fooditem.itemPrice)
                foodIds.append(fooditem.itemID)
                menuIDs.append(menu[4])
        print(foodnames)
        print(itemPrices)
        print(foodIds)
        print(menuIDs)
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

        print(formsInput)
        print(subtotals)
        # Create a key-value pair in the session dictionary to store the total
        session['FormsInput'] = formsInput
        session['ItemsIds'] = foodIds
        session['MenuIds'] = menuIDs
        session['ProductTotal'] = sum(subtotals)
        # This key-value pair ensures that when the checkout page is refreshed,
        # the customer is not charged more than once
        session['orderMade'] = False

        return render_template("menu.html",check = check,numberType=numberType,databaseitems=menus,foodnames= foodnames,itemPrices=itemPrices,formsInput=formsInput, doge=doge,total = subtotals,sumitem = sumitem,shopbutton=shopbutton, placebutton=placebutton,numbers=numbers)

    elif placebutton.submit.data:
        return checkout()

    return render_template("menu.html",check = check,numberType=numberType,databaseitems=menus, doge=doge, sumitem=sumitem,shopbutton=shopbutton, placebutton=placebutton,numbers=numbers)

@app.route('/checkout')
@login_required('CUSTOMER')
def checkout():
    # Get the value stored in the session['ProductTotal'] and store it in cartTotal
    # If there is no item on the cart, return a message for them to return to menu
    # Otherwise, process the order.

    # If the checkout menu is refreshed, the user will be redirected to menu page
    cartTotal = session.get('ProductTotal')
    custaccbal = current_user.acctBal
    vip_price = 0
    if cartTotal == 0:

        return '<p>You have not selected anything, go back to <a href="menu">menu</a>!!!<p>'
    else:
        if session.get('orderMade'):
            return redirect(url_for('menu'))
        else:
            if cartTotal > custaccbal:
                message = 'Seems like you need a new job.'
            else:
                vip = current_user.statusVIP
                if vip:
                    message = "You are VIP. 10% Discount was applied"
                    vip_price = cartTotal*.90
                    current_user.acctBal = current_user.acctBal - vip_price
                    custaccbal = current_user.acctBal
                    db.session.commit()
                else:
                    message = "You are a regular customer. Get VIP status to get 10% discount!"
                    current_user.acctBal = current_user.acctBal - cartTotal
                    custaccbal = current_user.acctBal
                    db.session.commit()

                #Process Order, meaning create Order
                new_order = Order(username=current_user.username,
                                  delivererID=1008, #ICHWAN PUT YOUR RANDOM DELIVERY GUYS FUNCTION
                                    totalPrice=session.get('ProductTotal'),
                                    isDelivered=False)
                db.session.add(new_order)
                db.session.commit()
                #Now using the new order insert the bought items in the database
                foodIds = session.get('ItemsIds')
                menuIds = session.get('MenuIds')
                foodQty = session.get('FormsInput')

                print(new_order.orderID,"ORDERRRRRR ID")

                for i in range(0,len(foodQty)):
                    if not(foodQty[i] == 0):
                        new_order_detail = OrderDetail(orderID=new_order.orderID,
                                               menuID=menuIds[i],
                                               itemID=foodIds[i],
                                               itemQty=foodQty[i],
                                               itemRating=1,
                                               itemComments=None)
                        db.session.add(new_order_detail)
                        db.session.commit()

                print("IVE MADE IT!")
                session['orderMade'] = True
    return render_template("checkout.html", user = current_user.username, total=cartTotal,custaccbal=custaccbal , message=message,vip=vip, vip_price=vip_price)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = login1()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(username=form.username.data).first()
        if customer:
            if customer.password == form.password.data:
                if customer.activated:
                    login_user(customer)
                    return redirect(url_for('home'))
                else:
                    flash("You have been kicked out of the system customer!")
                    print("Not active customer!")
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
                if employee.activated == True:
                    login_user(employee)
                    print("EMPLY LOGGED IN")
                    return redirect(url_for('home'))
                else:
                    print("Not active employee")
                    flash("You have been fired! Go away employee")
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
        return '<h1> You are logged in, %s %s as %s </h1>' % (current_user.firstName, current_user.lastName,current_user.get_user_type())
    else:
        return '<h1> You are logged out </h1>'


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/profile',methods=['GET', 'POST'])
@login_required('CUSTOMER')
def user_profile():
    orders = []
    orders = get_customer_orders(current_user.username)
    numorders = len(orders)
    orderprice = []
    for items in orders:
        price = items.totalPrice
        orderprice.append(price)
    totalprice = sum(orderprice)
    if numorders >= 50:
        flagorder = 1
    else:
        flagorder = 0
    if totalprice >= 500:
        flagprice = 1
    else:
        flagprice = 0
    ####
    details = []
    displayOrders = []
    numbers = [0, 1, 2, 3, 4]
    ordersmade = get_customer_orders(current_user.username)
    for order in ordersmade:
        order_detail = get_order_details(order.orderID)
        complaintOrder = complaint(prefix=order.username + str(order.orderID))
        complaintOrder.employee.choices = get_pair_id_employee()
        displayOrders.append((order.orderID,complaintOrder,current_user.username))
        details.append(order_detail)

    displayfood = []
    for detail in details:
        for item in detail:
            food = FoodItem.query.filter(FoodItem.itemID == item.itemID).first()
            rateForm = giveRating(prefix=str(food.itemName)+str(item.orderID))
            displayfood.append((food.itemName,food.itemPrice,food.itemRating,item.orderID,item.itemQty,food.itemPict,rateForm))

    for form in displayOrders:
        if form[1].submit.data:
            print("IM HERE SUBMIT")
            Complaint.query.filter_by(complaintID=form[0]).delete()  # Remove if existing
            db.session.commit()
            #Now replace complaint or create new one
            new_complaint = Complaint(orderID=form[0],
                                           username=form[2],
                                           emplID=form[1].employee.data,
                                           comment=form[1].comp.data,
                                           isGood=form[1].isGood.data)
            print("Complaint Made")
            db.session.add(new_complaint)
            db.session.commit()
            return redirect(url_for("user_profile"))
    ####
    return render_template("profile.html",numbers=numbers, user = current_user, displayOrders=displayOrders, displayfood=displayfood, numorders=numorders, totalprice = totalprice,flagorder=flagorder,flagprice=flagprice)

  
@app.route('/managerPage',methods=['GET', 'POST'])
@login_required('MANAGER')
def manager_page():
    managerForm = managerButtons(prefix="Manager Buttons") #Creates buttons for manager functionalities
    demotions = get_pair_demotion_emplName() #Gets employee demonitions
    closeRequests = get_close_requests()
    newCustomers = get_new_customers_notifications()
    vipNotification = get_VIP_notifications()
    dropVipNotification = drop_customer_VIP_list()
    deregisterNotification = get_deregister_warnings_customers()
    # This function inputs the items of a menu and a keyword.
    # Creates the number of forms neccesary for the specific menu list using the keyword.
    def make_forms_for_items(listOfItems, keyword):
        formlist = []
        for i in range(0, len(listOfItems)):
            form = accept_issuewarning(prefix=str(keyword) + str(i))  # Create a unique form with the keyword for each menu item
            formlist.append(form)
        return formlist

    # Complaints and Compliments
    complaints = get_complaints()
    showCom = []
    for comp in complaints:
        if comp.accepted == None:
            buttons = accept_issuewarning(prefix=str(comp.complaintID))
            showCom.append((comp.isGood, comp.orderID, comp.username, comp.comment,buttons,comp.complaintID))
            # print(showCom)


    print(len(showCom))
    for i in range(len(showCom)):
        print (showCom[i][5])
    print(showCom)

    #The following "accepts" the complaint or "warms" the customer
    for i in range(0, len(showCom)):
        if showCom[i][4].accept.data:
            print("Accepted",i)
            accept_complaint(showCom[i][5]) #getting error
            return redirect(url_for("manager_page"))
        elif showCom[i][4].warning.data:
            decline_complaint(showCom[i][5])
            return redirect(url_for("manager_page"))

    for req in newCustomers:
        if req[2].accept.data:
            activate_customer_account(req[0])
            return redirect(url_for('manager_page'))
        elif req[2].reject.data:
            reject_customer_account(req[0])
            return redirect(url_for('manager_page'))

    managerForm.employeeDropList.choices = get_pair_id_employee()
    managerForm.customerDropList.choices = get_pair_id_customer()

    if managerForm.hire.data:
        return redirect(url_for('hire'))
    elif managerForm.fire.data:
        fireEmplID = managerForm.employeeDropList.data
        fire_employee(fireEmplID)
        managerForm.employeeDropList.choices = get_pair_id_employee()
        managerForm.customerDropList.choices = get_pair_id_customer()
        return redirect(url_for('manager_page'))
        #return render_template("managerPage.html",managerForm=managerForm,showCom=showCom,demotions=demotions)

    elif managerForm.promoteE.data:
        employeeID = managerForm.employeeDropList.data
        promote_employee(employeeID)
        return redirect(url_for('manager_page'))
    elif managerForm.demoteE.data:
        employeeID = managerForm.employeeDropList.data
        demote_employee(employeeID)
        return redirect(url_for('manager_page'))
    elif managerForm.promoteC.data:
        customerUsername = managerForm.customerDropList.data
        promote_to_VIP(customerUsername)
        return redirect(url_for('manager_page'))
    elif managerForm.demoteC.data:
        customerUsername = managerForm.customerDropList.data
        demote_from_VIP(customerUsername)
        return redirect(url_for('manager_page'))
    elif managerForm.close.data:
        customerUsername = managerForm.customerDropList.data
        deactivate_customer_account(customerUsername)
        return redirect(url_for('manager_page'))

    return render_template("managerPage.html",managerForm=managerForm,showCom=showCom,demotions=demotions,closeRequests=closeRequests, newCustomers=newCustomers, vipNotification=vipNotification,dropVipNotification=dropVipNotification,deregisterNotification=deregisterNotification)


@app.route('/hire',methods=['GET', 'POST'])
@login_required('MANAGER')
def hire():
    hireform = hireEmployee()

    emplyTypeList = []
    employeeTypes = get_employee_types()
    for type in employeeTypes:
        emplyTypeList.append((type.typeID, type.description))

    hireform.typeDropList.choices = emplyTypeList

    salaryList = []
    salaries = get_salaries()

    for salary in salaries:
        salaryList.append((salary.salaryID, salary.hourBase))

    hireform.salaryDropList.choices = salaryList

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
                                    activated = True,
                                    password = hireform.password.data)
            db.session.add(new_employee)
            db.session.commit()
            print("Type plus sal:" + hireform.typeDropList.data + ' ' + hireform.salaryDropList.data)

            #Create menu if it is a chef
            if int(hireform.typeDropList.data) == 1: #Create empty menu for chef
                new_menu = Menu(chefID = new_employee.id,
                                menuName = "New Menu Coming Soon",
                                menuDesc = "Expect New Food!")
                db.session.add(new_menu)
                db.session.commit()
                print("MENU CREATED!")
            return redirect(url_for('manager_page'))

    return render_template("hire.html",hireForm=hireform)

  
@app.route('/chefPage',methods=['GET', 'POST'])
@login_required('CHEF')
def chef_Page():

    addToTheMenu = addToMenu(prefix="Add")
    removeFromMenu = deleteFromMenu(prefix="Delete")
    changeMenuFields = changeMenuInfo(prefix="Change")

    dropchoices = []
    fooditem = get_all_food_items()
    for item in fooditem:
        dropchoices.append((item.itemID, item.itemName))

    addToTheMenu.droplist.choices = dropchoices
    removeFromMenu.droplist.choices = dropchoices
    #We need to know which chef is cureently logged in to determine the menu or menus that he/she posseses
    listOfMenuItems = get_all_food_items_by_chef(current_user.id)

    menuForChef = get_all_menus_by_chef(current_user.id)
    menuID = int(menuForChef[0].menuID)
    menuDisplay = [current_user.firstName,current_user.lastName, menuForChef[0].menuName,menuForChef[0].menuDesc]

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

        return render_template("chefPage.html", add=addToTheMenu,delete = removeFromMenu,  menu=listOfMenuItems,changeMenuFields=changeMenuFields,menuDisplay=menuDisplay)

    elif removeFromMenu.submit.data:

        print("BEFORE DELETE:", get_table_size(MenuItem))

        MenuItem.query.filter_by(itemID=removeFromMenu.droplist.data,menuID=menuID).delete() #Make only one be removed
        db.session.commit()
        listOfMenuItems = get_all_food_items_by_chef(current_user.id)
        print("AFTER DELETE:", get_table_size(MenuItem))
        return render_template("chefPage.html", add=addToTheMenu,delete = removeFromMenu, menu=listOfMenuItems, changeMenuFields=changeMenuFields,menuDisplay=menuDisplay)

    elif changeMenuFields.submit.data:
        menuForChef[0].menuName = changeMenuFields.name.data
        menuForChef[0].menuDesc = changeMenuFields.description.data
        db.session.add(menuForChef[0])
        db.session.commit()
        return redirect(url_for('chef_Page'))
    elif changeMenuFields.addFoodItemsubmit.data:
        return redirect(url_for('add_Item'))

    return render_template("chefPage.html" ,add = addToTheMenu,delete = removeFromMenu, menu = listOfMenuItems, changeMenuFields=changeMenuFields,menuDisplay=menuDisplay)

@app.route('/addItem',methods=['GET', 'POST'])
@login_required('CHEF')
def add_Item():
    newItemForm = addFoodItem(prefix="New")
    pictures = [("f20.jpg","Picture f20"),("f21.jpg","Picture f21"),("f22.jpg","Picture f22"),("f23.jpg","Picture f23"),("f24.jpg","Picture f24"),("f25.jpg","Picture f25")]
    newItemForm.picture.choices = pictures

    if newItemForm.submit.data:
        #We prodive a generic description to mantain the look of menus
        genericDescription = 'Excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id.'
        #Save new item
        new_item = FoodItem(itemName=newItemForm.name.data,
                                itemDesc=genericDescription,
                                itemPrice=newItemForm.price.data,
                                itemPict=newItemForm.picture.data,
                                itemRating=0)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('chef_Page'))

    return render_template('addItem.html',newItemForm=newItemForm)

@app.route('/deliverPage',methods=['GET', 'POST'])
@login_required('DELIVERY')
def deliver_Page():
    return render_template("deliverPage.html")

  
@app.route('/addmoney', methods=['GET', 'POST'])
@login_required('CUSTOMER')
def addmoney():
    form = accountsetting()
    if form.validate_on_submit():
        current_user.acctBal = int(form.addmoney.data) + current_user.acctBal
        db.session.commit()
        return render_template("addmoney.html",form = form, user = current_user)
    return render_template("addmoney.html",form = form, user = current_user)


@app.route('/changeadd', methods=['GET', 'POST'])
@login_required('CUSTOMER')
def changeadd():
    form = changeaddress()
    if form.validate_on_submit():
        current_user.address = form.changeCurAdd.data
        db.session.commit()
        return render_template("changeadd.html",form = form, user = current_user)
    return render_template("changeadd.html",form = form, user = current_user)

@app.route('/changepassword', methods=['GET', 'POST'])
@login_required('CUSTOMER')
def changepassword():
    form = changepass()
    check = 0
    if form.validate_on_submit():
            if (current_user.password == form.oldpassword.data) and form.changeuserpass.data == form.confirm.data :
                current_user.password = form.confirm.data
                db.session.commit()
                check = 1
                return render_template("changepassword.html",form = form, user = current_user,check=check)
    return render_template("changepassword.html",form = form, user = current_user,check = check)

@app.route('/viewhistory', methods=['GET', 'POST'])
@login_required('CUSTOMER')
def vhistory():
    details = []
    displayOrders = []
    numbers = [0, 1, 2, 3, 4]
    ordersmade = get_customer_orders(current_user.username)
    for order in ordersmade:
        order_detail = get_order_details(order.orderID)
        complaintOrder = complaint(prefix=order.username + str(order.orderID))
        complaintOrder.employee.choices = get_pair_id_employee()
        displayOrders.append((order.orderID, complaintOrder, current_user.username))
        details.append(order_detail)

    displayfood = []
    for detail in details:
        for item in detail:
            food = FoodItem.query.filter(FoodItem.itemID == item.itemID).first()
            displayfood.append(
                (food.itemName, food.itemPrice, food.itemRating, item.orderID, item.itemQty, food.itemPict))

    for form in displayOrders:
        if form[1].submit.data:
            print("IM HERE SUBMIT")
            Complaint.query.filter_by(complaintID=form[0]).delete()  # Remove if existing
            db.session.commit()
            # Now replace complaint or create new one
            new_complaint = Complaint(orderID=form[0],
                                      username=form[2],
                                      emplID=form[1].employee.data,
                                      comment=form[1].comp.data,
                                      isGood=form[1].isGood.data)
            print("Complaint Made")
            db.session.add(new_complaint)
            db.session.commit()
            return redirect(url_for("user_profile"))
    check = 0
    if len(displayfood) == 0:
        check = 1
    return render_template("viewhistory.html", numbers=numbers, user=current_user, displayOrders=displayOrders,
                           displayfood=displayfood,check=check)

@app.route('/closeaccount', methods=['GET', 'POST'])
@login_required('CUSTOMER')
def close():
    return render_template("closeaccount.html", user = current_user)

@app.route('/terminate', methods=['GET', 'POST'])
@login_required('CUSTOMER')
def term():
    current_user.closerequest = 1
    db.session.commit()
    return redirect("logout")

@app.route('/argh', methods=['GET'])
@login_required('CUSTOMER')
def argh():
    return "You are either not logged in as a customer or not logged in at all"