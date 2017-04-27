from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
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
    numWarning = db.Column(db.Integer)
    statusVIP = db.Column(db.Boolean)
    deactivated = db.Column(db.Boolean)
    password = db.Column(db.Text)

class PaymentInfo(db.Model):
    __tablename__ = 'payment_infos'
    paymentID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(15), db.ForeignKey('customers.username'))
    paymentType = db.Column(db.String(10))
    acctNumber = db.Column(db.Integer)

    custRel = db.relationship('Customer', backref='paymentInfoRel')

class Menu(db.Model):
    __tablename__ = 'menus'
    menuID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chefID = db.Column(db.Integer, db.ForeignKey('employees.id'))
    menuName = db.Column(db.String(50))
    menuDesc = db.Column(db.Text)

    emplRel = db.relationship('Employee', backref='menuRel')

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

class FoodItem(db.Model):
    __tablename__ = 'food_items'
    itemID = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(50))
    itemDesc = db.Column(db.Text)
    itemPrice = db.Column(db.REAL)
    itemPict = db.Column(db.String(50))

class Order(db.Model):
    __tablename__ = 'orders'
    orderID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), db.ForeignKey('customers.username'))
    delivererID = db.Column(db.Integer, db.ForeignKey('employees.id'))
    totalPrice = db.Column(db.REAL)

    custRel = db.relationship('Customer', backref='orderRel')
    dboyRel = db.relationship('Employee', backref='orderRel')

class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    orderDetailID = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer, db.ForeignKey('orders.orderID'))
    menuID = db.Column(db.Integer, db.ForeignKey('menus.menuID'))
    itemID = db.Column(db.Integer, db.ForeignKey('food_items.itemID'))
    menuQty = db.Column(db.Integer)
    menuRating = db.Column(db.Integer)
    menuComments = db.Column(db.Text)

    __table_args__ = (db.CheckConstraint(sqltext='menuRating BETWEEN 1 and 5',
                                         name='valid_rating'),)

    ordRel = db.relationship('Order', backref='ordDetailRel')
    menuRel = db.relationship('Menu', backref='ordDetailRel')
    itemRel = db.relationship('FoodItem', backref='ordDetailRel')

class Employee(UserMixin, db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    lastName = db.Column(db.String(30))
    firstName = db.Column(db.String(30))
    emplType = db.Column(db.Integer, db.ForeignKey('employee_types.typeID'))
    numComplaint = db.Column(db.Integer)
    payGrade = db.Column(db.REAL)
    password = db.Column(db.Text)

    __table_args__ = (db.CheckConstraint(sqltext='numComplaint BETWEEN 0 and 3',
                                         name='complaint_range'),)

    emplTypeRel = db.relationship('EmployeeType', backref='employeeRel')

class EmployeeType(db.Model):
    __tablename__ = 'employee_types'
    typeID = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(30))

class SalaryBase(db.Model):
    __tablename__ = 'salary_bases'
    salaryID = db.Column(db.Integer, primary_key=True)
    hourBase = db.Column(db.REAL)
