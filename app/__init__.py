from flask import Flask
from flask_bs4 import Bootstrap
from flask_login import LoginManager
from .config import Config
from .auth import auth
from .models import UserModel

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicie sesión'
login_manager.login_message_category = 'warning'

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)

def create_app():
    app = Flask(__name__, template_folder='./templates', static_folder='./static')
    app.config.from_object(Config)
    bootstrap = Bootstrap(app)
    login_manager.init_app(app)
    app.register_blueprint(auth)
    return app