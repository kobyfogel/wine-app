import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET') or "1e79eb0s3d554c1fc1e979bf3c80dc22"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or "sqlite:///wine.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'login'

from wine.wine import routes
