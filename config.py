import os
from datetime import timedelta

class Config(object):
    SECRET_KEY = 'whZGhVqfGZccdwqWfBTriDrHzWozUCQD'

    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

 


class Debug(Config):
    # SQLAlchemy Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

    # Flask Login Configuration
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = timedelta(days=1)

    DEBUG = True


class Production(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://apc:apcekiti@localhost/apc'

    DEBUG = False


config_dict = {'Debug': Debug, 'Production': Production}
