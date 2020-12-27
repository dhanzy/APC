from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
security = Security()
admin = Admin(name='Dashboard', template_mode='bootstrap3', base_template='layout.html')
# Bootstrap = Bootstrap()

def register_extension(app):
    db.init_app(app)
    # Bootstrap.init_app(app)
    from APC.model import User, Role
    from APC.forms import ExtendedRegisterForm
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore, register_form=ExtendedRegisterForm)
    admin.init_app(app)


def register_bluprint(app):
    from APC.main.routes import main
    from APC.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(errors)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_extension(app)
    register_bluprint(app)
    return app
