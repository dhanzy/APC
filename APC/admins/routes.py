from flask import Blueprint, render_template
from flask_admin import  AdminIndexView, expose



admins = Blueprint('admins', __name__)


class AdminHomeView(AdminIndexView):
    @expose('/', methods=['GET'])