from flask import Blueprint,request, jsonify,session
from models import db,Users
from authlib.oauth2 import OAuth2Error
from OAuth2 import authorization, require_oauth

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

    return {
        'result': False,
        'code': 0
    }


@routes_blueprint.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
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