#!/usr/bin/env python
"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys

from flask import current_app
from run import app
from APC import bcrypt, db
from APC.model import User
import phonenumbers


try:
    raw_input
except:
    raw_input = input


def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.filter_by(role='super').first():
            create = raw_input('A user already exists! Create another? (y/n): ')
            if create == 'n':
                return
        while True:
            try:
                phone = raw_input('Enter Your Phone number: ')
                user = User.query.filter_by(phone=phone).first()
                number = phonenumbers.parse(phone)
                if not phonenumbers.is_valid_number(number):
                    print('The Phone number is not a valid one')
                    continue
                if user:
                    print('A user already exists with that phone number')
                    continue
                break
            except Exception as e:
                print('Error occured due to ' + str(e))
                exit(1)

        password = getpass("Password: ")
        assert password == getpass('Password (again):')

        user = User(
            phone=phone,
            city='Ado Ekiti',
            lga='Ekiti West',
            role='super',
            password = bcrypt.generate_password_hash(password).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        print('User {} added.'.format(phone))


if __name__ == '__main__':
    sys.exit(main())