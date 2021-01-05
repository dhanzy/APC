import os


import pdfkit
import secrets
from PIL import Image
from flask import Blueprint, render_template, make_response, redirect, session, request, flash, url_for
from flask_login import login_required, current_user, login_user, logout_user


from APC.model import User
from APC.forms import LoginForm, RegisterForm, UploadImageForm
from APC import db, bcrypt

main = Blueprint('main', __name__)


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


@main.route('/print/')
@login_required
def pdf_template():
    phone = current_user.phone
    user = User.query.filter_by(phone=phone).first()
    if user.image == 'default_profile.jpg':
        return redirect(url_for('main.index'))
    host = request.host
    rendered = render_template('pdfcontent2.html', user=user, host=host)
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"
    return response



# @main.route('/test/')
# @login_required
# def card2():
#     phone = current_user.phone
#     user = User.query.filter_by(phone=phone).first()
#     host = request.host
#     return render_template('pdfcontent2.html', user=user, host=host)
    


# @main.route('/profile/')
# @login_required
# def card():
#     user_id = current_user.get_id()
#     form = UploadImageForm()
#     user = User.query.filter_by(id=user_id).first()
#     return render_template('index.html', user=user, form=form)


@main.route('/card/', methods=['GET','POST'])
@login_required
def index():
    if current_user.role == 'admin' or current_user.role == 'super':    
        return redirect('/admin/')
    alert = None
    user_id = current_user.get_id()
    user = User.query.filter_by(id=user_id).first()
    form = UploadImageForm()
    if request.method == 'POST':
        if form.validate() and form.validate_on_submit():
            if form.profile_image.data:
                picture_file = save_picture(form.profile_image.data)
                user.image = picture_file
                db.session.commit()
                flash('Your Image has been uploaded', 'info')
                return redirect('/profile/')
        else:
            flash('Your Image was not uploaded', 'danger')
            return redirect('/profile/')
    if user.image == 'default_profile.jpg':
        alert = 'Upload your picture before you can print'
    return render_template('card.html', user=user, form=form, alert=alert)





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
            sex=form.sex.data, state=form.state.data, ward=form.ward.data, role='user',\
            city=form.city.data, lga=form.lga.data , password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered!", 'info')
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('security/register_user.html', form=form, title='Register APC')



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
                if form.remember.data == True:
                    login_user(remember=True)
                else:
                    login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
            else:
                flash("Invalid username/password.", 'danger')
        else:
            flash("Invalid username/password.", 'danger')
    return render_template('security/login_user.html', form=form, title='Login APC')





