import os


class Config(object):
    SECRET_KEY = 'adkbdbadbakdbahdbhfh'

    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

 


class Debug(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    DEBUG = True


class Production(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///database.db'
    DEBUG = False


config_dict = {'Debug': Debug, 'Production': Production}