import hashlib

from flask import Blueprint, request, current_app as app, session

from app.decorators import api_view
from app.models import db

blueprint = Blueprint("api_user", __name__)

@blueprint.route("/register", methods=["POST"])
@api_view
def register():
    username = request.form["username"]
    password = request.form["password"]

    if len(password) < 4:
        return {"message": "Password should be at least 4 characters long"}
    result = db.session.execute("SELECT 1 FROM users WHERE username = :username", {"username": username}).fetchone()
    if result is not None:
        return {"message": "That username is taken"}
    db.session.execute("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, 0)", {
        "username": username,
        "password": hashlib.sha256(password.encode("utf-8")).hexdigest()
    })
    db.session.commit()
    return {"message": "Success!"}

@blueprint.route("/login", methods=["POST"])
@api_view
def login():
    username = request.form["username"]
    password = request.form["password"]

    result = db.session.execute("SELECT id, password, is_admin FROM users WHERE username = :username AND password = :password", {
        "username": username,
        "password": hashlib.sha256(password.encode("utf-8")).hexdigest()
    }).fetchone()
    if result is None:
        return {"message": "Invalid credentials"}
    session["uid"] = result[0]
    session["is_admin"] = result[2] == 1
    return {"message": "Success!"}
