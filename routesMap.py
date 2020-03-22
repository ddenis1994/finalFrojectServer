import json

import requests as normalRequests
from authlib.oauth2 import OAuth2Error
from flask import Blueprint, request, session
from google.auth.transport import requests
from google.oauth2 import id_token

from models import db, Users
from OAuth2 import authorization

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


@routes_blueprint.route('/oauth/googleAuthorize', methods=['GET', 'POST'])
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
        print("debug data key " + r.text)
        # end debug#

        id_info = id_token.verify_oauth2_token(json_input["idToken"], requests.Request(), client_id)
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        user_id = id_info['sub']
        print(user_id)
    except ValueError:
        return {'result': False,
         'code': 1}
        pass

    return {'result': True,
            'code': 0}


@routes_blueprint.route('/oauth/authorize', methods=['GET', 'POST'])
def authorizeNormal():
    user = current_user()
    if request.method == 'GET':
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error
        return False
    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = Users.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return authorization.create_authorization_response(grant_user=grant_user)