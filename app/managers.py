from os import path
from app import manager
from config import basedir
from .models import *

# - This function will create a database with all of the dummy data in
#   it.
# - The @manager.command decorator allows this function to be run from
#   the command line by writing the name of the function So if you type
#   in `python Fourguys.py rebuild_database` on the command line, this
#   function will run.
# - When new models are added, and there's dummy data to fill it, a new
#   dictionary should be made in the dummy_files array that maps the
#   model to the dummy data file. The models are imported from the
#   statement `from .models import *`, and you map the model itself to a
#   dummy-data file. The rebuild_database handles the logic of filling
#   the tables up.
# - To keep this working correctly, the titles of the columns (the first
#   row in the csv file) should match the keys of the models exactly:
#   spaces, case, everything.
@manager.command
def rebuild_database():
    import csv
    db.drop_all()
    db.create_all()
    datadir = 'dummy-data'
    # These files should be in the dummy-data directory (or whichever
    # directory is currently the 'datadir'.
    dummy_files = [
        {'model': EmployeeType, 'file': 'emplTypes.csv'},
        {'model': SalaryBase, 'file': 'salaryBases.csv'},
        {'model': Employee, 'file': 'employees.csv'},
        {'model': Menu, 'file': 'menus.csv'},
        {'model': FoodItem, 'file': 'foodItems.csv'},
        {'model': MenuItem, 'file': 'menuItems.csv'},
        {'model': Customer, 'file': 'customers.csv'},
        {'model': Order, 'file': 'orders.csv'},
        {'model': OrderDetail, 'file': 'orderDetails.csv'}
    ]
    for thing in dummy_files:
        filename = path.join(basedir, datadir, thing['file'])
        with open(filename, newline='') as csvfile:
            # skipinitialspace for skipping spaces right after commas
            # (but not before commas).

            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                new_item = thing['model'](**row)
                db.session.add(new_item)
    db.session.commit()
