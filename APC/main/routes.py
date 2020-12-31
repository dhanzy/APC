import os


import pdfkit
import secrets
from PIL import Image
from flask import Blueprint, render_template, make_response, redirect, session, request, flash, url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, current_user, login_user, logout_user



from APC.model import User, Role
from APC.forms import LoginForm, RegisterForm, UploadImageForm
from APC import db, admin, bcrypt

main = Blueprint('main', __name__)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\\static\\images\\profile_pictures', picture_fn)
    size=(180,180)
    f = Image.open(form_picture)
    f.thumbnail(size)
    f.save(picture_path)
    return picture_fn


@main.route('/print/')
@login_required
def pdf_template():
    user = User.query.filter_by(email=email).first()
    host = request.host
    rendered = render_template('pdf_content.html', user=user, host=host)
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response

@main.route('/test/')
@login_required
def test():
    email = current_user.email
    user = User.query.filter_by(email=email).first()
    host = request.host
    rendered = render_template('pdf_content.html', user=user, host=host)
    return rendered

@main.route('/profile/', methods=['GET','POST'])
@login_required
def index():
    user_id = current_user.get_id()
    user = User.query.filter_by(id=user_id).first()
    form = UploadImageForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.profile_image.data:
                picture_file = save_picture(form.profile_image.data)
                os.remove(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\\static\\images\\profile_pictures', user.image))
                user.image = picture_file
                db.session.commit()
                flash('Your Image has been uploaded', 'info')
                return redirect('/profile/')
        else:
            flash('Your Image was not uploaded', 'danger')
            return redirect('/profile/')
    if user.image == 'default_profile.jpg':
        flash('Upload your picture before you can print', 'info')
    return render_template('index.html', user=user, form=form)


@main.route('/api/user/remove', methods=['POST'])
@login_required
def user_remove():
    """
    Remove a user from database
    """
    user_uid = request.form.get('user_uid')
    
    user = User.query.filter_by(id=int(user_uid)).first()
    if not user:
        print('Invalid User with id: ' + user_uid)
        return redirect('/admin/')
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('Successfully deleted user', 'success')
        return "User {} removed".format(user.phone)


@main.route('/register/', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user:
            flash('User already exists', 'info')
            return render_template('securtity/register_user.html', form=form)
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data ,phone=form.phone.data, \
            country=form.country.data, sex=form.sex.data, district=form.district.data, \
            constituency=form.constituency.data, state=form.state.data, ward=form.ward.data, city=form.city.data, \
            lga=form.lga.data , password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered!", 'info')
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('security/register_user.html', form=form)



@main.route('/logout/')
@login_required
def logout():
    """
    Log Out User
    """
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(phone=form.phone.data).first()
        if user:
			# password authentication
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
            else:
                flash("Invalid username/password.", 'danger')
        else:
            flash("Invalid username/password.", 'danger')
    return render_template('security/login_user.html', form=form)




admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(User, db.session))