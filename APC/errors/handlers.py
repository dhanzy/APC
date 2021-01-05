from flask import Blueprint, render_template, request

from APC import util

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    message = 'Experienced a 404 error, ' + str(request.referrer)
    util.log(message)
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    message = 'Experienced a 403 error, ' + str(request.referrer)
    util.log(message)
    return render_template('errors/403.html'), 403


@errors.app_errorhandler(400)
def error_400(error):
    message = 'Experienced a 400 error, ' + str(request.referrer)
    util.log(message)
    return render_template('errors/400.html'), 400


    
@errors.app_errorhandler(500)
def error_500(error):
    message = 'Experienced a 500 error, ' + str(request.referrer)
    util.log(message)
    return render_template('errors/500.html'), 500