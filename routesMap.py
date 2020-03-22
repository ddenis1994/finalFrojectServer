import crypt

from Tools.scripts import google
from flask import Blueprint, request, session

from models import db, Users

import json

from google.oauth2 import id_token
from google.auth.transport import requests

import requests as normalRequests

import base64
import cryptography.exceptions
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

GOOGLE_CLIENT_ID = "1029754518505-3u43tlle0uhqodueu4271n7rru15vdlf.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "3jA6N-qcK1W4NznlKGIQwW2Y"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)


def get_google_provider_cfg():
    return "https://accounts.google.com/o/oauth2/auth"


routes_blueprint = Blueprint('example_blueprint', __name__)


def current_user():
    if 'id' in session:
        uid = session['id']
        return Users.query.get(uid)
    return None


@routes_blueprint.route('/')
def hello_world():
    return 'Hello,werld!'


@routes_blueprint.route('/api/login', methods=['POST'])
def login():
    json_input = request.get_json()
    query = db.session.query(Users).filter(Users.username == json_input['username']).filter(
        Users.password_sha512 == json_input['password'])
    result = query.all()

    if (len(result) > 0):
        session['id'] = result[0].username
        return {
            'result': True,
            'code': 0
        }
    else:
        return {
            'result': False,
            'code': 0
        }


@routes_blueprint.route('/api/register', methods=['POST'])
def register():
    json_input = request.get_json()
    print(json_input['username'])
    u = Users(json_input['username'], json_input['email'], json_input['salt'], json_input['password'])
    db.session.add(u)
    db.session.commit()
    return {
        'result': False,
        'code': 0
    }


@routes_blueprint.route('/oauth/googleauthorize', methods=['GET', 'POST'])
def authorize():
    json_input = request.get_json()
    with open('./client_secret_google.json') as json_file:
        data = json.load(json_file)
        client_id = data['web']['client_id']
    try:
        # using debug verifier#
        verify_url = "https://oauth2.googleapis.com/tokeninfo"
        params = {'id_token': json_input["idToken"]}
        r = normalRequests.get(url=verify_url, params=params)
        print("key " + type(r.text))
        # end debug#

        id_info = id_token.verify_oauth2_token(json_input["idToken"], requests.Request(), client_id)
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        user_id = id_info['sub']
        print(user_id)
    except ValueError:

        pass

    return {'result': True,
            'code': 0}
