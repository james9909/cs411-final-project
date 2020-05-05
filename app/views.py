from bson import ObjectId
from flask import Blueprint, render_template, session, redirect, url_for, request, current_app as app, abort

from app.decorators import admin_required, login_required
from app.models import db

blueprint = Blueprint("views", __name__)

@blueprint.route("/", methods=["GET"])
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

@blueprint.route("/airbnb/<id>", methods=["GET"])
@login_required
def view_airbnb(id):
    airbnb = app.mongo_client["cs411"].airbnb.find_one({"_id": ObjectId(id)})
    if airbnb is None:
        return abort(404)

    pipeline = [
        {
            "$geoNear": {
                "near": airbnb["location"],
                "distanceField": "location"
            }
        },
        {
            "$lookup": {
                "from": "user_restaurants",
                "let": {
                    "localId": "$_id",
                },
                "pipeline": [
                    {
                        "$match": {
                            "$expr": {
                                "$and": [
                                    {
                                        "$eq": [
                                            "$restaurant_id",
                                            "$$localId"
                                        ]
                                    },
                                    {
                                        "$eq": [
                                            "$user_id",
                                            session["uid"]
                                        ]
                                    }
                                ]
                            }
                        }
                    }
                ],
                "as": "result"
            }
        },
        {
            "$project": {
                "name": 1,
                "is_favorited": {
                    "$cond": [
                        {
                            "$eq": ["$result", []]
                        },
                        False,
                        True
                    ]
                },
                "categories": 1
            }
        }
    ]

    nearby_restaurants = list(app.mongo_client["cs411"].restaurants.aggregate(pipeline))
    query = """
SELECT a.id, a.name, a.address, (ua.user_id IS NOT NULL) as is_favorited
FROM attractions a LEFT JOIN user_attractions ua ON (a.id = ua.attraction_id AND ua.user_id = :user_id)
ORDER BY (POW(a.latitude-:lat, 2)+POW(a.longitude-:long, 2))
    """
    nearby_attractions = db.session.execute(query, {
        "user_id": session["uid"],
        "lat": airbnb["location"]["coordinates"][0],
        "long": airbnb["location"]["coordinates"][1]
    }).fetchall()
    return render_template("airbnb.html", airbnb=airbnb, nearby_restaurants=nearby_restaurants, nearby_attractions=nearby_attractions)

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
