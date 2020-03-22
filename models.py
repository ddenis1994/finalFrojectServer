from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
import time


db = SQLAlchemy()



#          MODELS ####################
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password_sha512 = db.Column(db.String(128))
    lock = db.Column(db.Boolean,default=True)
    email = db.Column(db.String(120))
    salt = db.Column(db.String(16))


    def __init__(self, name=None, email=None,salt=None,password=None,lock=True):
        self.username = name
        self.email = email
        self.salt = salt
        self.password_sha512 = password
        self.lock = lock


    def __repr__(self):
        return "<User ( username = {}  " \
               "email = {} loch = {}"  \
               "salt = {} password = {}  )>".format(self.username,
                                                    self.email,
                                                    self.lock,
                                                    self.salt,
                                                    self.password_sha512
                                                        )

    def check_password(self, password):
        return password == self.password_sha512

    def get_user_id(self):
        return self.id


class Passwords(db.Model):
    __tablename__ = 'passwords'
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    service = db.Column(db.String(64))
    username_encrypt = db.Column(db.String(128))
    password_encrypt = db.Column(db.String(128))
    salt = db.Column(db.String(16))


    def __init__(self, userId=None, service=None,username_encrypt=None,password_encrypt=None,salt=True):
        self.userId = userId
        self.service = service
        self.username_encrypt = username_encrypt
        self.password_encrypt = password_encrypt
        self.salt = salt


    def __repr__(self):
        return "<Credentials ( userId = {}  " \
               "service = {}"  \
               "username = {} password = {}  salt = {})>".format(
                                                    self.userId,
                                                    self.service,
                                                    self.username_encrypt,
                                                    self.password_encrypt,
                                                    self.salt
                                                        )


class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('Users')


class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('Users')


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('Users')

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()