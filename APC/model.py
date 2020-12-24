from sqlalchemy import Column, String, Integer, Binary, Table, ForeignKey, Boolean, DateTime, Unicode
from flask_security import UserMixin, RoleMixin, current_user

from APC import db




role_users = db.Table(
    'role_user',
    db.Column('user_id', db.Integer(), ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(200))


    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Role %r>" % str(self.name)



class User(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True)
    firstname = db.Column(String(30))
    lastname = db.Column(String(30))
    email = db.Column(String(30), unique=True)
    sex = db.Column(String(10))
    password = db.Column(String(255))
    country = db.Column(String(50))
    state = db.Column(String(50))
    city = db.Column(String(50), nullable=False)
    lga = db.Column(String(50), nullable=False)
    image = db.Column(Unicode(150))
    ward = db.Column(String(50))
    phone = db.Column(String(50), nullable=False)
    active = db.Column(Boolean())
    roles = db.relationship('Role', secondary=role_users, backref=db.backref('user', lazy='dynamic'))

  
    def get_security_payload(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<User %r>" % str(self.email)        


class Country(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50))

    def __repr__(self):
        return "<Country %r>" % str(self.name)


class State(db.Model):
    id = db.Column(Integer, primary_key=True)
