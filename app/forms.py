from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SubmitField, SelectField, FloatField
from wtforms.validators import InputRequired, Email, Length, NumberRange
from .models import *

class signup(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    firstname = StringField('First name', validators=[InputRequired()])
    lastname = StringField('Last name', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    conpassword = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80), ])
    address = StringField('Address', validators=[InputRequired()])

class accountsetting(FlaskForm):
    addmoney = FloatField('Add balence', validators=[NumberRange (min=0)])

class changeaddress(FlaskForm):
    changeCurAdd = StringField('Address', validators=[InputRequired()])

class login1(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class loginEmployee(FlaskForm):
    employee = StringField('Employee Username', validators=[InputRequired(), Length(max=50)])
    password = PasswordField('Employee Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

class menu1(FlaskForm):
    qty = IntegerField('qty', validators=[InputRequired()], default=0)

class PlaceButton(FlaskForm):
    submit = SubmitField("Place Order")

class ShopButton(FlaskForm):
    submit = SubmitField("Add to Cart")

class addToMenu(FlaskForm):
    dropchoices = []
    fooditem = get_all_food_items()
    for item in fooditem:
        dropchoices.append((item.itemID, item.itemName))
    droplist = SelectField(label="Add Food Item", choices=dropchoices)
    submit = SubmitField("Add to Menu")

class deleteFromMenu(FlaskForm):
    dropchoices = []
    fooditem = get_all_food_items()
    for item in fooditem:
        dropchoices.append((item.itemID, item.itemName))
    droplist = SelectField(label="Remove Food Item", choices=dropchoices)
    submit = SubmitField("Remove from Menu")

class dropDownFood(FlaskForm):
    dropchoices = []
    fooditem = get_all_food_items()
    for item in fooditem:
        dropchoices.append((item.itemID,item.itemName))
    droplist = SelectField(label="Food Items", choices=dropchoices)

class managerButtons(FlaskForm):
    hire = SubmitField("Hire Employee")
    fire = SubmitField("Fire Employee")
    promoteE = SubmitField("Promote Employee")
    demoteE = SubmitField("Demote Employee")
    promoteC = SubmitField("Grant VIP")
    demoteC = SubmitField("Drop VIP")

class hireEmployee(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    firstname = StringField('First name', validators=[InputRequired()])
    lastname = StringField('Last name', validators=[InputRequired()])
    email = StringField('E-mail', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    conpassword = PasswordField('Confirm Password', validators=[InputRequired(), Length(min=8, max=80), ])
    address = StringField('Address', validators=[InputRequired()])




