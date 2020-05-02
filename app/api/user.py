import hashlib

from flask import Blueprint, request, current_app as app, session, flash

from app.decorators import api_view
from app.models import db

blueprint = Blueprint("api_user", __name__)

@blueprint.route("/register", methods=["POST"])
@api_view
def register():
    username = request.form["username"]
    password = request.form["password"]
    re_password = request.form["re_password"]
    error = None

    if not username:
        error = "Username is required."
    elif len(password) < 4:
        error = "Password should be at least 4 characters long."
    elif password != re_password:
        error = "Passwords don't match. Try again."
    elif db.session.execute("SELECT 1 FROM users WHERE username = :username", {"username": username}).fetchone() is not None:
        error = "User {} is already registered.".format(username)

    if error is None:
        db.session.execute("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, 0)",
            {
                "username": username,
                "password": hashlib.sha256(password.encode("utf-8")).hexdigest()
            })
        db.session.commit()
        return {}

    return {"status": 403, "message": error}

@blueprint.route("/login", methods=["POST"])
@api_view
def login():
    username = request.form["username"]
    password = request.form["password"]
    error = None

    result = db.session.execute("SELECT id, password, is_admin FROM users WHERE username = :username AND password = :password", {
        "username": username,
        "password": hashlib.sha256(password.encode("utf-8")).hexdigest()
    }).fetchone()
    if result is None:
        return {"status": 403, "message": "Invalid credentials"}

    session["uid"] = result[0]
    session["is_admin"] = result[2] == 1
    return {}
