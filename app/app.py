from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from . import auth
from . import views
from .models import User

app = Flask(__name__)
db =  MongoEngine()
login_manager = LoginManager()
app.config["MONGODB_SETTINGS"] = {
	"db":"littlify",
	"host":"localhost",
	"port":27017
}
app.secret_key = 'sdfsf&^%&*234'
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.objects.get(id=user_id)


app.register_blueprint(views.views,url_prefix='')
app.register_blueprint(auth.auth,url_prefix='')