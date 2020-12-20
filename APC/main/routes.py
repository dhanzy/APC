import os


import pdfkit
import secrets
from PIL import Image
from flask import Blueprint, render_template, make_response, redirect, session, request
from flask_admin.contrib.sqla import ModelView
from flask_security import login_required, current_user


from APC.model import User, Role
from APC.forms import ExtendedRegisterForm
from APC import db, admin, security

main = Blueprint('main', __name__)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static/images/profile', picture_fn)
    size=(180,180)
    f = Image.open(form_picture)
    f.thumbnail(size)
    f.save(picture_path)
    return picture_fn


@main.route('/print/')
@login_required
def pdf_template():
    email = current_user.email
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

@main.route('/')
@login_required
def index():
    email = current_user.email
    user = User.query.filter_by(email=email).first()
    print('Request ', request.host)
    return render_template('index.html', user=user)

admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(User, db.session))