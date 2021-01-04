from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_bootstrap import Bootstrap

# Database
db = SQLAlchemy()


# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'


# Bcrypt
bcrypt = Bcrypt()

# Admin
admin = Admin(name='Dashboard', template_mode='bootstrap3')

# Bootstrap = Bootstrap()

def register_extension(app):
    from APC.model import User
    from APC.admins.routes import AdminHomeView
    
    db.init_app(app)
    # Bootstrap.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    admin.init_app(app, index_view=AdminHomeView(name='Dashboard'))


def register_bluprint(app):
    from APC.main.routes import main
    from APC.errors.handlers import errors
    from APC.admins.routes import admins
    from APC.api.routes import api

    app.register_blueprint(main)
    app.register_blueprint(admins)
    app.register_blueprint(errors)
    app.register_blueprint(api)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extension(app)
    register_bluprint(app)
    return app
