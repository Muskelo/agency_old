import os

class Configuration(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')

    # SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://user:password@127.0.0.1:3306/db"
    SQLALCHEMY_TRACK_MODIFICATION = True

