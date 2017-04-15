from os import path

# For paths to files relative to this script.
basedir = path.abspath(path.dirname(__file__) )

SECRET_KEY = 'ThisIsTheMostAwesomeSafeKey123!'

# path.join is used to say 'basedir/database.db' without worrying if
# this will be run on a UNIX or Windows system.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(basedir, 'database.db')

SQLALCHEMY_TRACK_MODIFICATIONS = False
