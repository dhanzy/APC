import os


import secrets
from PIL import Image
from flask import request, flash, Blueprint, redirect
from flask_login import login_required, current_user


from APC import db, bcrypt
from APC import util
from APC.model import User


api = Blueprint('api', __name__)



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/images/profile_pictures', picture_fn)
    size=(180,180)
    f = Image.open(form_picture)
    f.thumbnail(size)
    f.save(picture_path)
    return picture_fn



@api.route('/api/user/image', methods=['POST'])
def user_image():
    """
    Add user image to database
    """


@api.route('/api/user/remove/', methods=['POST'])
@login_required
def user_remove():
    """
    Remove a user from database
    """
    user_uid = request.form.get('user_uid')
    
    user = User.query.filter_by(id=int(user_uid)).first()
    if not user:
        return redirect('/admin/')
    if user:
        if user.role == 'admin' or user.role == 'super':
            flash('The user you specified is an admin. You can\'t remove an admin!', 'info')
            return redirect('/admin/')
        db.session.delete(user)
        db.session.commit()
        return "User {} removed".format(user.phone)


@api.route('/api/user/password/', methods=['POST'])
@login_required
def change_password():
    print('Form: ', request.form)
    if request.form.get('password') != request.form.get('confirm_password'):
        flash('Confirm Password does not match password field','danger')
        return redirect(request.referrer)
    password = request.form.get('password')
    user_id = request.form.get('user_id')
    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            flash('User does not exist', 'danger')
            return redirect(request.referrer)        
    except:
        flash('Unable to change password!', 'danger')
        return redirect(request.referrer)
    
    if password == request.form.get('confirm_password'):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        if user.role == 'admin'  or user.role == 'super':
            if user.id == current_user.id or user.role == 'super':
                print('Password Hashed!: ', hashed_password)
                user.password = hashed_password
                db.session.commit()
                print('Comitted')
                message = '"user {}:{}:{}"  password has been changed'.format(str(user.id), user.firstname, user.phone)
                util.log(message)
                flash('User password has been updated', 'info')
                return redirect(request.referrer)
            else:
                message = '"user {}:{}:{}"  password could not be changed'.format(str(user.id), user.firstname, user.phone)
                util.log(message)
                flash('Cannot change Users password', 'danger')
                return redirect(request.referrer)
        user.password = hashed_password
        db.session.commit()
        message = '"user {}:{}:{}"  password has been changed'.format(str(user.id), user.firstname, user.phone)
        util.log(message)
        flash('User password has been updated', 'info')
        return redirect(request.referrer)
    flash('Password Not Changed', 'danger')
    return redirect(request.referrer)