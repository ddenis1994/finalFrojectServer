from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error, client
from flask import Blueprint, request, jsonify, session

from OAuth2 import authorization, require_oauth
from models import db, Users

from google.oauth2 import id_token
from google.auth.transport import requests
import httplib2
from apiclient import discovery


routes_blueprint = Blueprint('example_blueprint', __name__)
GOOGLE_CLIENT_SECRET = "3jA6N-qcK1W4NznlKGIQwW2Y"
GOOGLE_CLIENT_ID = "1029754518505-3u43tlle0uhqodueu4271n7rru15vdlf.apps.googleusercontent.com"

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
    query = db.session.query(Users).filter(Users.username == json_input['username']).filter(Users.password_sha512 == json_input['password'])
    result = query.all()


    if(len(result) > 0):
        session['id']=result[0].username
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
    u=Users(json_input['username'],json_input['email'],json_input['salt'],json_input['password'])
    db.session.add(u)
    db.session.commit()
    return {
        'result': False,
        'code': 0
    }


@routes_blueprint.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    json_input = request.get_json()
    print(json_input['authId'])
    try:
        idinfo  = id_token.verify_oauth2_token(json_input['authId'], requests.Request(), GOOGLE_CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
    except ValueError:
    # Invalid token
            pass
    if not request.headers.get('X-Requested-With'):
        return {"result":False,"code":443}
    credentials = client.credentials_from_clientsecrets_and_code(
        GOOGLE_CLIENT_SECRET,
        ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
        json_input['authId'])
    http_auth = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http=http_auth)
    appfolder = drive_service.files().get(fileId='appfolder').execute()

    userid = credentials.id_token['sub']
    email = credentials.id_token['email']
    print(userid,email)

    """ 
    user = current_user()
    if request.method == 'GET':
        try:
            grant = authorization.validate_consent_request(end_user=user)
        except OAuth2Error as error:
            return error.error
        return "error"
    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = Users.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return authorization.create_authorization_response(grant_user=grant_user)
"""


@routes_blueprint.route('/logout')
def logout():
    del session['id']
    return "sucsees"



@routes_blueprint.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@routes_blueprint.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


@routes_blueprint.route('/api/me')
@require_oauth('profile')
def api_me():
    user = current_token.user
    return jsonify(id=user.id, username=user.username)

@routes_blueprint.route("/login/callback")
def callback():
    print("test")
    # Get authorization code Google sent back to you
    code = request.args.get("code")


