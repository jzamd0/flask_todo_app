from os import environ

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from .models import *

app = Flask(__name__)
migrate = Migrate()
login_manager = LoginManager()

load_dotenv()

app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = environ.get(
    "SQLALCHEMY_TRACK_MODIFICATIONS"
)

app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


from .routes.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

from .routes.main import main as main_blueprint

app.register_blueprint(main_blueprint)

from .routes.error import error as error_blueprint

app.register_blueprint(error_blueprint)
