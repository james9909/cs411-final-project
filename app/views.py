from bson import ObjectId
from flask import Blueprint, render_template, session, redirect, url_for, request, current_app as app, abort

from app.decorators import admin_required, login_required
from app.models import db

blueprint = Blueprint("views", __name__)

@blueprint.route("/", methods=["GET"])
def index():
    search_name = request.args.get("search_name", "", type=str)
    max_price = request.args.get("max_price", "", type=float)
    lowest_rating = request.args.get("lowest_rating", "", type=int)
    query = {}
    if search_name != "":
        query["name"] = {
                "$regex": ".*{}.*".format(search_name),
                "$options": "i"
                }

    if max_price != "":
        query["price"] = {
                "$lte": max_price
            }

    if lowest_rating != "":
        query["rating"] = {
                "$gte": lowest_rating
            }

    data = app.mongo_client["cs411"].airbnb.find(query)
    return render_template("index.html", airbnbs=data)

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

@blueprint.route("/profile")
@login_required
def profile():
    restaurant_query = [
        {
            "$match": {
                "user_id": session["uid"]
            }
        },
        {
            "$lookup": {
                "from": "restaurants",
                "localField": "restaurant_id",
                "foreignField": "_id",
                "as": "restaurant"
            }
        },
        {
            "$unwind": "$restaurant"
        },
        {
            "$project": {
                "_id": 0,
                "restaurant": 1
            }
        }
    ]
    attraction_query = """
    SELECT a.id, a.name
    FROM attractions a INNER JOIN user_attractions ua ON a.id = ua.attraction_id AND ua.user_id = :user_id
    """
    favorite_attractions = db.session.execute(attraction_query, {"user_id": session["uid"]}).fetchall()
    favorite_restaurants = list(x["restaurant"] for x in app.mongo_client["cs411"].user_restaurants.aggregate(restaurant_query))
    return render_template("profile.html", favorite_attractions=favorite_attractions, favorite_restaurants=favorite_restaurants)

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

@blueprint.route("/restaurant/<id>")
@login_required
def view_restaurant(id):
    restaurant = app.mongo_client["cs411"].restaurants.find_one({"_id": ObjectId(id)})
    if restaurant is None:
        return abort(404)

    return render_template("restaurant.html", restaurant=restaurant)

@blueprint.route("/attraction/<id>")
@login_required
def view_attraction(id):
    attraction = db.session.execute("SELECT * FROM attractions WHERE id = :id", {"id": id}).first()
    if attraction is None:
        return abort(404)

    return render_template("attraction.html", attraction=attraction)
