from flask import Blueprint, render_template, session, redirect, url_for, request, current_app as app

from app.decorators import admin_required, login_required
from app.models import db

blueprint = Blueprint("views", __name__)

@blueprint.route("/", methods=["GET"])
@login_required
def index():
    airbnbs = app.mongo_client["cs411"].airbnb.find()
    return render_template("index.html", airbnbs=airbnbs)

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
@admin_required
def admin_attractions():
    search_name = request.args.get("search_name", "", type=str)
    if search_name != "":
        result = db.session.execute("SELECT id, name, address, rating, latitude, longitude FROM attractions WHERE name LIKE :name", {
            "name": "%" + search_name + "%"
        }).fetchall()
    else:
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

@blueprint.route("/admin/restaurants")
@admin_required
def admin_restaurants():
    search_name = request.args.get("search_name", "", type=str)
    query = {}
    if search_name != "":
        query = {
            "name": {
                "$regex": ".*{}.*".format(search_name),
                "$options": "i"
            }
        }
    data = app.mongo_client["cs411"].restaurants.find(query)
    return render_template("admin/restaurants.html", restaurants=data)


@blueprint.route("/admin/airbnbs")
@admin_required
def admin_airbnbs():
    search_name = request.args.get("search_name", "", type=str)
    query = {}
    if search_name != "":
        query = {
            "name": {
                "$regex": ".*{}.*".format(search_name),
                "$options": "i"
            }
        }
    data = app.mongo_client["cs411"].airbnb.find(query)
    return render_template("admin/airbnb.html", airbnbs=data)
