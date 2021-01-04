import os


import secrets
from PIL import Image
from flask import request, flash, Blueprint, redirect
from flask_login import login_required


from APC import db
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


@api.route('/api/user/remove', methods=['POST'])
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


