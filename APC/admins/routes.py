import os
from datetime import datetime
import functools

import pdfkit
import secrets
from PIL import Image
from flask import Blueprint, render_template, request, url_for, make_response, flash, redirect, abort
from flask_admin import  AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, current_user
 

from APC import admin, bcrypt
from APC.model import User, db
from APC.forms import RegisterForm, UploadImageForm, ChangePassword


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


def admin_required(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'admin' or current_user.role == 'super':
            return function(*args, **kwargs)
        elif not current_user.is_authenticated:
            return redirect(url_for('main.login'))
        else:
            return abort(403)



class AdminHomeView(AdminIndexView):
    @login_required
    @expose('/', methods=['GET','POST'])
    def index(self):
        print('Role: ', current_user.role)
        if current_user.role != 'admin' and current_user.role != 'super':
            return abort(403)
        users = User.query.all()
        n = len(users)
        return self.render('admin/index.html', users=users, n=n)


@admin_required
@admins.route('/admin/profile/<user_id>', methods=['GET','POST'])
def profile(user_id):
    if current_user.is_authenticated:
        alert = None
        form = RegisterForm()
        form2 = UploadImageForm()
        form3 = ChangePassword()
        if request.method == 'POST':
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                    flash('Invalid User', 'danger')
                    return redirect(request.referrer)
            if form2.submit_btn.data and form2.validate() and form2.validate_on_submit:
                if form2.profile_image.data:
                    if user.role == 'admin' or user.role == 'super' and current_user.id != user.id:
                        flash('Can\'t change another admins image', 'danger')
                        return redirect(request.referrer)
                    picture_file = save_picture(form2.profile_image.data)
                    user.image = picture_file
                    db.session.commit()
                    flash('Your Image has been uploaded', 'info')
                    return redirect(request.referrer)

            # print('Checking form3')
            # if form3.submit.data and form3.validate_on_submit:
            #     print('Form3 Gotten')
            #     hashed_password = bcrypt.generate_password_hash(form3.password.data).decode('utf-8')
            #     print('Encrypted password')
            #     if user.role == 'admin'  or user.role == 'super':
            #         print('User is an admin')
            #         if user.id == current_user.id or user.role == 'super':
            #             user.password == hashed_password
            #             db.session.commit()
            #             flash('User password has been updated', 'info')
            #             return redirect(request.referrer)
            #         else:
            #             flash('Cannot change Users password', 'danger')
            #             return redirect(request.referrer)
            #     user.password == hashed_password
            #     db.session.commit()
            #     flash('User password has been updated', 'info')
            #     return redirect(request.referrer)

            if form.submit.data and form.validate_on_submit:
                if user.role == 'admin' or user.role == 'super' and current_user.id != user.id:
                        flash('Can\'t alter another admins details', 'danger')
                        return redirect(request.referrer)
                user.firstname = form.firstname.data
                user.lastname = form.lastname.data
                user.phone = form.phone.data
                user.sex = form.sex.data
                user.state = form.state.data
                user.lga = form.lga.data
                user.city = form.city.data
                user.ward = form.ward.data

                db.session.commit()
                flash('User account has been Updated', 'info')
                return redirect(request.referrer)
            
            
            


            form.firstname.data = user.firstname
            form.lastname.data = user.lastname
            form.phone.data = user.phone
            form.sex.data = user.sex
            form.state.data = user.state
            form.lga.data = user.lga
            form.city.data = user.city
            form.ward.data = user.ward

            if user.image == 'default_profile.jpg':
                alert = 'Upload User picture before you can print'
            return render_template('admin/profile.html', form=form, user=user, form2=form2, form3=form3, alert=alert)
        elif request.method=='GET':
            user = User.query.filter_by(id=int(user_id)).first()
            if not user:
                return abort(403)
            form.firstname.data = user.firstname
            form.lastname.data = user.lastname
            form.phone.data = user.phone
            form.sex.data = user.sex
            form.state.data = user.state
            form.lga.data = user.lga
            form.city.data = user.city
            form.ward.data = user.ward

            if user.image == 'default_profile.jpg':
                alert = 'Upload User picture before you can print'
            return render_template('admin/profile.html', form=form, user=user, form2=form2,form3=form3, alert=alert)
    elif current_user.is_authenticated:
        return abort(403)
    else:
        return redirect('/')



@admin_required
@admins.route('/admin/print/<user_id>')
def pdf_template(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    print('Image: ', user.image)
    if user.image == 'default_profile.jpg':
        return redirect(url_for('main.index'))
    host = request.host
    rendered = render_template('pdfcontent2.html', user=user, host=host)
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response



class SuperView(ModelView):
    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.role == 'super':
            return False
        if current_user.role == 'super':
            return True

        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect('/admin/')

    can_export = False
    can_delete = True
    edit_modal = True
    create_modal = True
    details_modal = True


admin.add_view(SuperView(User, db.session))
