from app import app
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# class user(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(15))
#     lastname = db.Column(db.String(50))
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(50))
#     address = db.Column(db.String(50))
#     card = db.Column(db.String(50))
#
# class items(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     itemname= db.Column(db.String(15), unique=True)
#     price = db.Column(db.Integer)
#     chef = db.Column(db.String(15))
#     itemdes = db.Column(db.String(50))

class Customer(db.Model):
    __tablename__ = 'customers'
    # customerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), primary_key=True)
    lastName = db.Column(db.String(30))
    firstName = db.Column(db.String(30))
    email = db.Column(db.String(30))
    address = db.Column(db.String(50))
    zipcode = db.Column(db.Integer)
    state = db.Column(db.String(2))
    statusVIP = db.Column(db.Boolean)
    accountBal = db.Column(db.REAL)
    numWarning = db.Column(db.Integer)
    custPict = db.Column(db.BLOB)
    cardNumber = db.Column(db.Integer)
    password = db.Column(db.Text)

class Menu(db.Model):
    __tablename__ = 'menus'
    menuID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chefID = db.Column(db.Integer, db.ForeignKey('employees.emplID'))
    menuName = db.Column(db.String(50))
    menuDesc = db.Column(db.Text)
    menuPrice = db.Column(db.REAL)
    menuRating = db.Column(db.Integer)
    menuPict = db.Column(db.BLOB)
    #__table_args__ = (db.CheckConstraint(menuRating in range(0, 6), name='Valid rating'), {})

    emplRel = db.relationship('Employee', backref='menuRel')

class Order(db.Model):
    __tablename__ = 'orders'
    orderID = db.Column(db.Integer, primary_key=True)
    customerID = db.Column(db.String(15), db.ForeignKey('customers.username'))
    delivererID = db.Column(db.Integer, db.ForeignKey('employees.emplID'))
    menuID = db.Column(db.Integer, db.ForeignKey('menus.menuID'))
    menuQty = db.Column(db.Integer)
    menuComment = db.Column(db.Text)
    menuRating = db.Column(db.Integer)
    #__table_args__ = (db.CheckConstraint(menuRating in range(0, 6), name='Valid rating'), {})

    custRel = db.relationship('Customer', backref='orderRel')
    dboyRel = db.relationship('Employee', backref='orderRel')
    menuRel = db.relationship('Menu', backref='orderRel')


class Employee(db.Model):
    __tablename__ = 'employees'
    emplID = db.Column(db.Integer, primary_key=True)
    emplType = db.Column(db.Integer, db.ForeignKey('employee_types.typeID'))
    rating = db.Column(db.Integer)
    payGrade = db.Column(db.REAL)
    #__table_args__ = (db.CheckConstraint(rating in range(0, 6), name='Valid rating'), {})

    emplTypeRel = db.relationship('EmployeeType', backref='employeeRel')

class EmployeeType(db.Model):
    __tablename__ = 'employee_types'
    typeID = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(30))