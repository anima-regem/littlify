from flask_mongoengine import MongoEngine
from flask_login import UserMixin
db = MongoEngine()

class User(UserMixin, db.Document):
    email = db.EmailField(required=True,unique=True)
    password = db.StringField(required=True)
    verified = db.BooleanField(required=True,default=False)

class Data(db.Document):
    short = db.StringField(required=True,unique=True,max_length=7)
    url = db.StringField(required=True)
    owner = db.ReferenceField(User)