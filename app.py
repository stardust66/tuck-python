import os
import json
from flask import (Flask, render_template, redirect, url_for, request,
                   abort, make_response)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect, generate_csrf, CSRFError

app = Flask(__name__)

CSRFProtect().init_app(app)

# Configurations
# Using environmental variables
app.config.update(
    SECRET_KEY=os.environ["SECRET_KEY"],
    SQLALCHEMY_DATABASE_URI=os.environ["DATABASE_URL"],
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from models import User

# Add csrf_token
@app.after_request
def add_csrf_to_cookie(response):
    """Adds csrf_token to cookie

    Add to cookies with every response.
    """
    return_response = make_response(response)
    return_response.set_cookie("csrf_token", generate_csrf())
    return return_response

@app.errorhandler(CSRFError)
def handle_csrf_error():
    return "CSRF Error!"

# Pages
@app.route('/')
def index(message=""):
    return render_template("index.html", message=message)

@app.route('/register')
def register(message=""):
    return render_template("register.html", message=message)

@app.route('/login/validate', methods=["POST"])
def validate_login():
    email = request.form.get("email")
    password = request.form.get("password")

    if "" in [email, password]:
        return index("Empty email or password.")

    success, name = validate_password(email, password)
    if success:
        return add_user_to_cookies(redirect(url_for("index")), email, name)
    else:
        return index("Wrong password.")


# Request Handlers
@app.route('/register/validate', methods=["POST"])
def validate_register():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    if "" in [first_name, email, password]:
        # This message can be made more specific
        return register("Wrong input.")

    # No SQL code needed
    new_user = User(first_name, last_name, email, password)
    db.session.add(new_user)
    db.session.commit()

    return add_user_to_cookies(redirect(url_for("index")), email, first_name)

# Helper Functions
def add_user_to_cookies(response, email, name):
    return_response = make_response(response)
    return_response.set_cookie("user_email", email)
    return_response.set_cookie("user_name", name)
    return return_response

def validate_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user:
        return (user.check_password(password), user.first_name)
    else:
        return (False, None)
