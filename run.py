from flask_migrate import Migrate


from config import config_dict
from APC import create_app, db


config = config_dict.get('Debug')


app = create_app(config)
Migrate(app, db, render_as_batch=True)


if __name__ == '__main__':
    app.run()
