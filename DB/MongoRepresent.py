import mongoengine as me

class User(me.Document):
    username=me.StringField(required=True)
    userUniq=me.StringField(required=True)
