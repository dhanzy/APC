from sqlalchemy import Column, String, Integer, Binary, Table, ForeignKey, Boolean, DateTime, Unicode
from flask_login import UserMixin


from APC import db, login_manager



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model, UserMixin):
    id = db.Column(Integer, primary_key=True)
    firstname = db.Column(String(30))
    lastname = db.Column(String(30))
    phone = db.Column(String(50), nullable=False, unique=True)
    sex = db.Column(String(10))
    state = db.Column(String(50))
    ward = db.Column(String(50))
    city = db.Column(String(50), nullable=False)
    lga = db.Column(String(50), nullable=False)
    password = db.Column(String(255))
    image = db.Column(Unicode(150), default='default_profile.jpg')
    active = db.Column(Boolean())
    role = db.Column(String(50))

  
    def get_security_payload(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'phone': self.phone,
        }

    def __str__(self):
        return self.phone

    def __repr__(self):
        return "<User %r>" % str(self.phone)


class Country(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50))

    def __repr__(self):
        return "<Country %r>" % str(self.name)


class State(db.Model):
    id = db.Column(Integer, primary_key=True)
