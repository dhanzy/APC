import os
from datetime import datetime

import pdfkit
import secrets
from PIL import Image
from flask import Blueprint, render_template, request, url_for, make_response, flash, redirect
from flask_admin import  AdminIndexView, expose, BaseView
from flask_login import login_required, current_user
 

from APC.model import User, db
from APC.forms import RegisterForm, UploadImageForm


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
        return self.render('admin/index.html', users=users)



@admins.route('/admin/profile/<user_id>', methods=['GET','POST'])
@login_required
def profile(user_id):
    if current_user.is_authenticated:
        alert = None
        form = RegisterForm()
        form2 = UploadImageForm()
        if request.method == 'POST':
            user = User.query.filter_by(id=int(user_id)).first()
            if form2.submit_btn.data and form2.validate() and form2.validate_on_submit:
                if form2.profile_image.data:
                    picture_file = save_picture(form2.profile_image.data)
                    user.image = picture_file
                    db.session.commit()
                    flash('Your Image has been uploaded', 'info')
                    return redirect(request.referrer)
            if form.submit.data and form.validate_on_submit:
                user.firstname = form.firstname.data
                user.lastname = form.lastname.data
                user.phone = form.phone.data
                user.sex = form.sex.data
                user.state = form.state.data
                user.lga = form.lga.data
                user.city = form.city.data
                user.ward = form.ward.data
                user.country = form.country.data
                
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
            form.country.data = user.country

            if user.image == 'default_profile.jpg':
                alert = 'Upload User picture before you can print'
            return render_template('admin/profile.html', form=form, user=user, form2=form2, alert=alert)
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
            form.country.data = user.country

            if user.image == 'default_profile.jpg':
                alert = 'Upload User picture before you can print'
            return render_template('admin/profile.html', form=form, user=user, form2=form2, alert=alert)
    elif current_user.is_authenticated:
        return abort(403)
    else:
        return redirect('/')



@admins.route('/admin/print/<user_id>')
@login_required
def pdf_template(user_id):
    user = User.query.filter_by(id=int(user_id)).first()
    print('Image: ', user.image)
    if user.image == 'default_profile.jpg':
        return redirect(url_for('main.index'))
    host = request.host
    rendered = render_template('pdf_content.html', user=user, host=host)
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response