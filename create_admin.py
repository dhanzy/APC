#!/usr/bin/env python
"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys

from flask import current_app
from run import app
from APC import bcrypt, db
from APC.model import User

def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print 'A user already exists! Create another? (y/n):',
            create = raw_input()
            if create == 'n':
                return

        print 'Enter Phone Number: ',
        phone = raw_input()
        password = getpass("Password: ")
        assert password == getpass('Password (again):')

        user = User(
            phone=phone, 
            password=bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print 'User added.'


if __name__ == '__main__':
    sys.exit(main())