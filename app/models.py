import faketime
from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import func, desc
db = SQLAlchemy(app)


class Customer(UserMixin, db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), unique=True)
    lastName = db.Column(db.String(30))
    firstName = db.Column(db.String(30))
    address = db.Column(db.String(50))
    city = db.Column(db.String(30))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.Integer)
    email = db.Column(db.String(30), unique=True)
    contactNum = db.Column(db.Integer)
    acctBal = db.Column(db.REAL)
    numWarning = db.Column(db.Integer, default=0)
    statusVIP = db.Column(db.Boolean, default=0)
    activated = db.Column(db.Boolean, default=0)
    password = db.Column(db.Text)

    def __repr__(self):
        return '<customerID: %s, username: %s>' % (self.id, self.username)

    def get_user_type(self):
        return 'CUSTOMER'

    def get_user_type(self):
        return "CUSTOMER"

class PaymentInfo(db.Model):
    __tablename__ = 'payment_infos'
    paymentID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(15), db.ForeignKey('customers.username'))
    paymentType = db.Column(db.String(10))
    acctNumber = db.Column(db.Integer)

    custRel = db.relationship('Customer', backref='paymentInfoRel')

    def __repr__(self):
        return '<paymentID: %s, username: %s>' % (self.paymentID, self.username)


class Menu(db.Model):
    __tablename__ = 'menus'
    menuID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chefID = db.Column(db.Integer, db.ForeignKey('employees.id'))
    menuName = db.Column(db.String(50))
    menuDesc = db.Column(db.Text)

    emplRel = db.relationship('Employee', backref='menuRel')

    def __repr__(self):
        return '<menuID: %s, menu: %s>' % (self.menuID, self.menuName)


# A relationship between menus and food items. States which food items
# are available in which menus.

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    menuItemID = db.Column(db.Integer, primary_key=True)
    menuID = db.Column(db.Integer, db.ForeignKey('menus.menuID'), primary_key=True)
    itemID = db.Column(db.Integer, db.ForeignKey('food_items.itemID'), primary_key=True)
    menuItemRating = db.Column(db.Integer)

    __table_args__ = (db.CheckConstraint(sqltext='menuItemRating BETWEEN 1 AND 5',
                                         name='valid_rating'),)

    menuRel = db.relationship('Menu', backref='menuItemRel')
    foodItemRel = db.relationship('FoodItem', backref='menuItemRel')

    def __repr__(self):
        return '<menuID: %s, itemID: %s>' % (self.menuID, self.itemID)


# A table of different food items. Has the basic characteristics of food
class FoodItem(db.Model):
    __tablename__ = 'food_items'
    itemID = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(50))
    itemDesc = db.Column(db.Text)
    itemPrice = db.Column(db.REAL)
    itemPict = db.Column(db.String(50))
    itemRating = db.Column(db.INTEGER)

    def __repr__(self):
        return '<itemID: %s, itemName: %s>' % (self.itemID, self.itemName)


class Order(db.Model):
    __tablename__ = 'orders'
    orderID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), db.ForeignKey('customers.username'))
    delivererID = db.Column(db.Integer, db.ForeignKey('employees.id'))
    orderDate = db.Column(db.DateTime, default=faketime.FakeTime.get_now())
    totalPrice = db.Column(db.REAL)
    isDelivered = db.Column(db.Boolean)

    custRel = db.relationship('Customer', backref='orderRel')
    dboyRel = db.relationship('Employee', backref='orderRel')

    def __repr__(self):
        return '<orderID: %s, total: %s>' % (self.orderID, self.totalPrice)


    @property
    def order_date(self):
        return self.orderDate

    @order_date.setter
    def order_date(self, data):
        self.orderDate = datetime.strptime(data, '%Y-%m-%d %H:%M')


class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    orderDetailID = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer, db.ForeignKey('orders.orderID'))
    menuID = db.Column(db.Integer, db.ForeignKey('menus.menuID'))
    itemID = db.Column(db.Integer, db.ForeignKey('food_items.itemID'))
    itemQty = db.Column(db.Integer)
    itemRating = db.Column(db.Integer)
    itemComments = db.Column(db.Text)

    __table_args__ = (db.CheckConstraint(sqltext='itemRating BETWEEN 1 and 5',
                                         name='valid_rating'),)

    ordRel = db.relationship('Order', backref='ordDetailRel')
    menuRel = db.relationship('Menu', backref='ordDetailRel')
    itemRel = db.relationship('FoodItem', backref='ordDetailRel')

    def __repr__(self):
        return '<orderID: %s, menuID: %s, itemID: %s, qty: %s>' % (self.orderID, self.menuID, self.itemID, self.itemQty)


class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    lastName = db.Column(db.String(30))
    firstName = db.Column(db.String(30))
    emplType = db.Column(db.Integer, db.ForeignKey('employee_types.typeID'))
    numComplaint = db.Column(db.Integer, default=0)
    numDemotion = db.Column(db.Integer, default=0)
    payGrade = db.Column(db.Integer, db.ForeignKey('salary_bases.salaryID'))
    activated = db.Column(db.Boolean, default=True)
    password = db.Column(db.Text)

    __table_args__ = (db.CheckConstraint(sqltext='numComplaint BETWEEN 0 and 3',
                                         name='complaint_range'),
                      db.CheckConstraint(sqltext='numDemotion BETWEEN 0 and 2',
                                         name='demotion_range'),)

    emplTypeRel = db.relationship('EmployeeType', backref='employeeRel')
    salaryBaseRel = db.relationship('SalaryBase', backref='employeeRel')

    def __repr__(self):
        return '<emplID: %s, username: %s, emplType: %s>' % (self.id, self.username, self.emplType)

    def get_user_type(self):
        if self.emplType == 0:
            return 'MANAGER'
        elif self.emplType == 1:
            return 'CHEF'
        else:
            return 'DELIVERY'

    def get_user_type(self):
        if self.emplType == 0:
            return "MANAGER"
        elif self.emplType == 1:
            return "CHEF"
        else:
            return "DELIVERY"

class EmployeeType(db.Model):
    __tablename__ = 'employee_types'
    typeID = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(30))

    def __repr__(self):
        return '<typeID: %s, description: %s>' % (self.typeID, self.description)


class SalaryBase(db.Model):
    __tablename__ = 'salary_bases'
    salaryID = db.Column(db.Integer, primary_key=True)
    hourBase = db.Column(db.REAL)

    def __repr__(self):
        return '<salaryID: %s, hour base: %s>' % (self.salaryID, self.hourBase)


class Complaint(db.Model):
    __tablename__ = 'complaints'
    complaintID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), db.ForeignKey('customers.username'))
    emplID = db.Column(db.Integer, db.ForeignKey('employees.id'))
    orderID = db.Column(db.Integer, db.ForeignKey('orders.orderID'))
    comment = db.Column(db.Text)
    isGood = db.Column(db.Boolean)
    accepted = db.Column(db.Boolean)

    custRel = db.relationship(Customer, backref='complaintRel')
    emplRel = db.relationship(Employee, backref='complaintRel')
    orderRel = db.relationship(Order, backref='complaintRel')

    def __repr__(self):
        return '<complaintID: %s, isGood: %s>' % (self.complaintID, self.isGood)


# MENU-RELATED QUERIES

# returns all food items that are available in the database
def get_all_food_items():
    return FoodItem.query.all()


# returns the five most ordered food items
def get_five_most_popular():
    stmt = db.session.query(OrderDetail.itemID, func.count(OrderDetail.itemID).label('total'))\
        .group_by(OrderDetail.itemID)\
        .limit(5).subquery('stmt')
    return FoodItem.query\
        .join(stmt, stmt.c.itemID == FoodItem.itemID)\
        .order_by(desc(stmt.c.total)).all()


# returns all food items that are part of a menu
def get_all_food_items_by_menu(menuID):
    return FoodItem.query\
        .join(MenuItem, MenuItem.itemID == FoodItem.itemID)\
        .filter(MenuItem.menuID == menuID).all()


# returns all food items that are associated with a chef
def get_all_food_items_by_chef(chefID):
    return FoodItem.query\
        .join(Menu, Menu.menuID == MenuItem.menuID)\
        .join(MenuItem, MenuItem.itemID == FoodItem.itemID)\
        .filter(Menu.chefID == chefID).all()


# returns all menus created by a chef
def get_all_menus_by_chef(chefID):
    return Menu.query\
        .filter(Menu.chefID == chefID).all()


# CUSTOMER-RELATED QUERIES

# returns the last five items ordered by the customer
def get_top_five_items(username):
    stmt = OrderDetail.query\
        .join(Order, Order.orderID == OrderDetail.orderID)\
        .filter(Order.username == username)\
        .subquery('stmt')
    return FoodItem.query\
        .filter(FoodItem.itemID == stmt.c.itemID)\
        .limit(5).all()


# returns all orders that has been made by a customer
def get_customer_orders(username):
    return Order.query\
        .filter(Order.username == username).all()


# returns the order detail for a given order number
def get_order_details(orderID):
    return OrderDetail.query\
        .filter(OrderDetail.orderID == orderID).all()


# returns the food item detail for an order
def get_food_item_from_order(orderID, itemID):
    return OrderDetail.query\
        .filter(OrderDetail.orderID == orderID, OrderDetail.itemID == itemID)\
        .first()


# update the rating for a food item ordered
# as part of an order
def rate_food_item_ordered(orderID, itemID, rating):
    food_item = get_food_item_from_order(orderID, itemID)
    food_item.itemRating = rating
    db.session.add(food_item)
    db.session.commit()


# update the comment for a food item ordered
# as part of an order
def comment_food_item_ordered(orderID, itemID, comment):
    food_item = get_food_item_from_order(orderID, itemID)
    food_item.itemComments = comment
    db.session.add(food_item)
    db.session.commit()


# post a new complaint for a specific order and/or chef
def make_complaint(orderID, emplID, username, comments, isGood):
    stmt = Complaint()
    stmt.orderID = orderID
    stmt.emplID = emplID
    stmt.username = username
    stmt.comment = comments
    stmt.isGood = isGood
    db.session.add(stmt)
    db.session.commit()


# CHEF-RELATED QUERIES

# calculate the average rating of food item
# associated with a menu from all the records
# in the `order_details` table
def get_cumulative_food_item_rating(menuID, itemID):
    stmt = db.session.query(func.avg(OrderDetail.itemRating))\
        .filter(OrderDetail.itemID == itemID, OrderDetail.menuID == menuID)\
        .scalar()
    return round(stmt)


# DELIVERY BOY QUERY

# returns all orders that has been assigned
# to a delivery person
def get_all_orders_by_delivery_person(emplID):
    return Order.query\
        .filter(Order.delivererID == emplID).all()


# allow the delivery boy to check that
# the order has been successfully delivered
def check_delivered(orderID):
    stmt = Order.query.filter(Order.orderID == orderID).first()
    stmt.isDelivered = True
    db.session.add(stmt)
    db.session.commit()


# MANAGER-RELATED QUERIES

# returns all new customers request
# for accounts
def get_all_new_customers():
    return Customer.query.filter(Customer.activated == False).all()


# deactivate a customer account
def deactivate_customer_account(username):
    stmt = Customer.query.filter(Customer.username == username).first()
    stmt.activated = False
    db.session.add(stmt)
    db.session.commit()


# activate a customer account
def activate_customer_account(username):
    stmt = Customer.query.filter(Customer.username == username).first()
    stmt.activated = True
    db.session.add(stmt)
    db.session.commit()


# promote a customer to VIP Status
def promote_to_VIP(username):
    stmt = Customer.query.filter(Customer.username == username).first()
    stmt.statusVIP = True
    db.session.add(stmt)
    db.session.commit()


# demote a customer from VIP Status
def demote_from_VIP(username):
    stmt = Customer.query.filter(Customer.username == username).first()
    stmt.statusVIP = False
    db.session.add(stmt)
    db.session.commit()


# returns the total amount of money
# that has been spent by a customer
def total_money_spent(username):
    stmt = db.session.query(func.sum(Order.totalPrice)) \
        .filter(Order.username == username) \
        .scalar()
    return 0 if stmt is None else round(stmt)


def get_number_of_orders(username):
    stmt = db.session.query(func.count(Order.username))\
        .filter(Order.username == username).scalar()
    return 0 if stmt is None else stmt


# return all employees in the database
def get_all_employees():
    return Employee.query.all()


# increase the pay grade of the employee
def promote_employee(emplID):
    stmt = Employee.query.filter(Employee.id == emplID).first()
    stmt.payGrade += 1
    db.session.add(stmt)
    db.session.commit()


# decrease the pay grade of the employee and
# increment the numDemotion field by one
def demote_employee(emplID):
    stmt = Employee.query.filter(Employee.id == emplID).first()
    if stmt.numDemotion in range(0, 2):
        stmt.payGrade -= 1
        stmt.numDemotion += 1
    db.session.add(stmt)
    db.session.commit()


# deactivate the employee account, effectively firing them
def fire_employee(emplID):
    stmt = Employee.query.filter(Employee.id == emplID).first()
    stmt.activated = False
    db.session.add(stmt)
    db.session.commit()

    
# calculate the average rating for all
# food items cooked by a chef
def get_total_rating(chefID):
    stmt = db.session.query(func.avg(OrderDetail.itemRating)) \
        .join(Menu, OrderDetail.menuID == Menu.menuID) \
        .filter(Menu.chefID == chefID) \
        .scalar()
    return None if stmt is None else round(stmt)


# returns the number of days since the chef
# receive their latest order
def get_days_since_last_order(chefID):
    stmt = db.session.query(func.max(Order.orderDate))\
        .join(OrderDetail, Order.orderID == OrderDetail.orderID)\
        .join(Menu, OrderDetail.menuID == Menu.menuID)\
        .filter(Menu.chefID == chefID)\
        .scalar()
    return None if stmt is None else (faketime.FakeTime.get_now() - stmt).days


# returns all complaints that has not been processed
# (i.e. `accepted` field is Null/None)
def get_all_complaints():
    return Complaint.query.filter(Complaint.accepted == None).all()


# accept the complaint or compliment that has been posted
# by a customer and increment or decrement the number of complaint
# for the corresponding employee by one, respectively
def accept_complaint(complaintID):
    complaint_stmt = Complaint.query.filter(Complaint.complaintID == complaintID).first()
    empl = Employee.query.filter(Employee.id == complaint_stmt.emplID).first()
    complaint_stmt.accepted = True
    if complaint_stmt.isGood:
        if empl.numComplaint in range(0, 3):
            empl.numComplaint -= 1
    else:
        if empl.numComplaint in range(0, 3):
            empl.numComplaint += 1
    db.session.add_all([complaint_stmt, empl])
    db.session.commit()


# decline the complaint that has been posted by a customer
# and increment the number of warning to that customer by one
def decline_complaint(complaintID):
    complaint_stmt = Complaint.query.filter(Complaint.complaintID == complaintID).first()
    cust = Customer.query.filter(Customer.username == complaint_stmt.username).first()
    complaint_stmt.accepted = False
    if complaint_stmt.isGood:
        db.session.add(complaint_stmt)
    else:
        if cust.numWarning in range(0, 3):
            cust.numWarning += 1
            db.session.add_all([complaint_stmt, cust])
    db.session.commit()

    
#Checks if fooditem exists in a menu. True if it does. False otherwise.
def is_food_item_exist(menuID, itemID):
    result = MenuItem.query.filter(MenuItem.itemID == itemID, MenuItem.menuID == menuID).all()
    if not result:
        return False
    else:
        return True


# Function to get size of a table
def get_table_size(table):

    table_elements = table.query.count()
    return table_elements


def get_employee_types():
    emplTypes = EmployeeType.query.all()
    return emplTypes


def get_salaries():
    salaries = SalaryBase.query.all()
    return salaries


def get_employees():
    employees = Employee.query.all()
    return employees


def get_customers():
    customers = Customer.query.all()
    return customers
