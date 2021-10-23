import os
from datetime import timedelta

import dotenv

dotenv.load_dotenv()
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')

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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)

    DEBUG = False


config_dict = {'Debug': Debug, 'Production': Production}
