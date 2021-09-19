from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy

import json
import os
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

import requests

app = Flask(__name__)
app.config.from_object("project.config.Config")
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
db = SQLAlchemy(app)
# User session management setup: https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

from .models import User # after db init()
from .auth import auth as auth_blueprint 
from .main import main as main_blueprint
# blueprint for non-auth(main) and auth(auth) routes in our app
app.register_blueprint(main_blueprint)
app.register_blueprint(auth_blueprint)

# Flask boostrap setup
#Bootstrap(app)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)

