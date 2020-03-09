from sqlalchemy import Column, Integer, String,Boolean
from flask import Flask, request, jsonify,session
from models import db
from routesMap import routes_blueprint
from OAuth2 import config_oauth
import os




def setup_app(app):
    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables():
        db.create_all()

    db.init_app(app)
    config_oauth(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.secret_key=os.urandom(24)
    # register the blueprint
    app.register_blueprint(routes_blueprint)


def create_app(config=None):
    app = Flask(__name__)
    setup_app(app)
    app.run(debug=True)

    return app

if __name__ == '__main__':
    create_app(config=None)