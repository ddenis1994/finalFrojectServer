import requests
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
from sqlalchemy import Column, Integer, String,Boolean
from flask import Flask, request, jsonify,session
from werkzeug.utils import redirect

from models import db,Users
from routesMap import routes_blueprint
from OAuth2 import config_oauth
import os

GOOGLE_CLIENT_ID = "1029754518505-3u43tlle0uhqodueu4271n7rru15vdlf.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "3jA6N-qcK1W4NznlKGIQwW2Y"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

login_manager = LoginManager()
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

app = Flask(__name__)

def setup_app(app):
    # Create tables if they do not exist already
    @app.before_first_request
    def create_tables():
        u = Users("testu", "test", "salt", "1")
        db.session.add(u)
        db.session.commit()
        db.create_all()

    db.init_app(app)
    login_manager.init_app(app)
    config_oauth(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['GOOGLE_CLIENT_ID']=GOOGLE_CLIENT_ID
    app.config['GOOGLE_CLIENT_SECRET']=GOOGLE_CLIENT_SECRET
    app.config['GOOGLE_DISCOVERY_URL']=GOOGLE_DISCOVERY_URL
    app.secret_key=os.urandom(24)
    # register the blueprint
    app.register_blueprint(routes_blueprint)


def create_app(config=None):

    setup_app(app)
    app.run(debug=True)

    return app

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    print("try call back")
    code = request.args.get("code")
    return True

@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

if __name__ == '__main__':
    create_app(config=None)

