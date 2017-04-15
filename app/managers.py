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
#   model to the dummy data file.
@manager.command
def rebuild_database():
    import csv
    db.drop_all()
    db.create_all()
    datadir = 'dummy-data'
    # These files should be in the dummy-data directory (or whichever
    # directory is currently the 'datadir'.
    dummy_files = [
        { 'model': items, 'file': 'menuitems.csv' },
        { 'model': user, 'file': 'users.csv' }
    ]
    for thing in dummy_files:
        filename = path.join(basedir, datadir, thing['file'])
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile, skipinitialspace=True)
            for row in reader:
                new_item = thing['model'](**row)
                db.session.add(new_item)
                #print(new_item)
    db.session.commit()