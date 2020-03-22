import os


from flask import Flask
from flask_login import LoginManager

from models import db
from routesMap import routes_blueprint

app = Flask(__name__)



login_manager = LoginManager()



def setup_app(app):
    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables():
        db.create_all()

    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)

    app.secret_key=os.urandom(24)
    # register the blueprint
    app.register_blueprint(routes_blueprint)


def create_app(config=None):
    setup_app(app)
    app.run(debug=True)
    return app



if __name__ == '__main__':
    create_app(config=None)

