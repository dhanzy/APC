import os
from datetime import datetime

from PIL import Image
from flask import Blueprint, render_template, request, url_for
from flask_admin import  AdminIndexView, expose, BaseView
from flask_security import login_required
 

from APC.model import User
from APC.forms import RegisterForm


admins = Blueprint('admins', __name__)



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



class AdminHomeView(AdminIndexView):
    @login_required
    @expose('/', methods=['GET','POST'])
    def index(self):
        users = User.query.all()
        print('USers: ', users)
        return self.render('admin/index.html', users=users)


@login_required
@admins.route('/admin/profile/<user_id>')
def profile(user_id):
    if current_user.is_authenticated:
        form = RegisterForm()
        if request.method == 'POST':
            if form.validate_on_submit:
                user_id = request.form.get('user_id')
                user = User.query.filter_by(id=int(user_id)).first()
                if form.profile_image.data:
                    picture_file = save_picture(form.profile_image.data)
                    if picture_file != 'default_profile.jpg':
                        os.remove(current_user.profile_image)
                    user.image = picture_file
                user.firstname = form.firstname.data
                user.lastname = form.lastname.data
                user.email = form.email.data
                
                db.session.commit()
                flash('User account has been Updated')
                return redirect(request.refe)
        elif request.method=='GET':
            form.firstname.data = current_user.firstname
            form.lastname.data = current_user.lastname
            form.phone.data = current_user.phone
        return self.render('admin/profile.html', form=form)
    elif current_user.is_authenticated:
        return abort(403)
    else:
        return redirect('/')
