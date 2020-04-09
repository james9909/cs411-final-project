from flask import Blueprint, render_template, session, redirect, url_for

from app.models import db

blueprint = Blueprint("views", __name__)

@blueprint.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@blueprint.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@blueprint.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@blueprint.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")

@blueprint.route("/admin/attractions")
def admin_attractions():
    result = db.session.execute("SELECT id, name, address, rating, latitude, longitude FROM attractions").fetchall()
    data = []
    for row in result:
        data.append({
            "id": row[0],
            "name": row[1],
            "address": row[2],
            "rating": row[3],
            "latitude": row[4],
            "longitude": row[5]
        })
    return render_template("admin/attractions.html", attractions=data)
