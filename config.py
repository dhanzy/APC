import os


class Config(object):
    SECRET_KEY = 'adkbdbadbakdbahdbhfh'

    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security Configuration
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'aeffafyabvuavuu'
    SECURITY_LOGIN_URL = '/login/'
    SECURITY_LOGOUT_URL = '/logout/'
    SECURITY_REGISTER_URL = '/register/'
    SECURITY_REGISTER_USER_TEMPLATE = 'security/register_user.html'
    SECURITY_TRACKABLE = False


class Debug(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    DEBUG = True


class Production(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///database.db'
    DEBUG = False


config_dict = {'Debug': Debug, 'Production': Production}