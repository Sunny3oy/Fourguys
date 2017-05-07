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

    def __repr__(self):
        return '<customerID: %s, username: %s}>' % (self.id, self.username)


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


class FoodItem(db.Model):
    __tablename__ = 'food_items'
    itemID = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(50))
    itemDesc = db.Column(db.Text)
    itemPrice = db.Column(db.REAL)
    itemPict = db.Column(db.String(50))

    def __repr__(self):
        return '<itemID: %s, itemName: %s>' % (self.itemID, self.itemName)


class Order(db.Model):
    __tablename__ = 'orders'
    orderID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), db.ForeignKey('customers.username'))
    delivererID = db.Column(db.Integer, db.ForeignKey('employees.id'))
    totalPrice = db.Column(db.REAL)

    custRel = db.relationship('Customer', backref='orderRel')
    dboyRel = db.relationship('Employee', backref='orderRel')

    def __repr__(self):
        return '<orderID: %s, total: %s>' % (self.orderID, self.totalPrice)


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
    numComplaint = db.Column(db.Integer)
    payGrade = db.Column(db.REAL)
    password = db.Column(db.Text)

    __table_args__ = (db.CheckConstraint(sqltext='numComplaint BETWEEN 0 and 3',
                                         name='complaint_range'),)

    emplTypeRel = db.relationship('EmployeeType', backref='employeeRel')

    def __repr__(self):
        return '<emplid: %s, username: %s, emplType: %s>' % (self.id, self.username, self.emplType)


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


# MENU-RELATED QUERIES

# returns all food items that are available in the database
def get_all_food_items():
    return FoodItem.query.all()


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


# rate a specific food item that has been ordered
def rate_food_item_ordered(orderID, itemID, rating):
    food_item = OrderDetail.query\
        .filter(OrderDetail.orderID == orderID, OrderDetail.itemID == itemID)\
        .first()
    food_item.itemRating = rating
    db.session.add(food_item)
    db.session.commit()


def comment_food_item_ordered(orderID, itemID, comment):
    pass

# returns all orders that has been assigned to a delivery person
def get_all_orders_by_delivery_person(emplID):
    return Order.query\
        .filter(Order.delivererID == emplID).all()


def get_cumulative_food_item_rating(foodItem, chefID):
    pass
