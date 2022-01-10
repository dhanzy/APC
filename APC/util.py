import logging
from flask_login import current_user

def log(msg, level='debug'):
    user_fmt = 'Anonymous'
    if current_user.is_authenticated:
        user_fmt = '{}:{}:{}'.format(str(current_user.id), current_user.firstname, current_user.phone)
    logging.basicConfig(filename='apcekiti_access.log', level=logging.DEBUG, format='%(asctime)s - ' + user_fmt +' - %(message)s', filemode='a')
    logger = logging.getLogger(__name__)
    getattr(logger, level if hasattr(logger, level) else 'debug')(msg)
    