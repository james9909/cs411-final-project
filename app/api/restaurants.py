from bson.objectid import ObjectId
from flask import Blueprint, request, current_app as app, session

from app.decorators import api_view, login_required, admin_required

blueprint = Blueprint("api_restaurants", __name__)

@blueprint.route("/", methods=["POST"])
@api_view
@admin_required
def add_restaurant():
    db = app.mongo_client["cs411"]
    document = {
        "name": request.form["name"],
        "rating": float(request.form["rating"]),
        "location": {"type": "Point", "coordinates": [float(request.form["latitude"]), float(request.form["longitude"])]},
        "address": request.form["address"],
        "categories": list(map(str.strip, request.form["categories"].split(","))),
        "yelp_url": request.form["yelp_url"]
    }
    db.restaurants.insert_one(document)
    return {"message": "Success!"}

@blueprint.route("/<id>", methods=["POST"])
@api_view
@admin_required
def update_restaurant(id):
    db = app.mongo_client["cs411"]
    query = {
        "$set": {
            "name": request.form["name"],
            "rating": float(request.form["rating"]),
            "location": {"type": "Point", "coordinates": [float(request.form["latitude"]), float(request.form["longitude"])]},
            "address": request.form["address"],
            "categories": list(map(str.strip, request.form["categories"].split(","))),
            "yelp_url": request.form["yelp_url"]
        }
    }
    db.restaurants.update_one({"_id": ObjectId(id)}, query)
    return {"message": "Success!"}


@blueprint.route("/<id>", methods=["DELETE"])
@api_view
@admin_required
def delete_restaurant(id):
    db = app.mongo_client["cs411"]
    db.restaurants.delete_one({"_id": ObjectId(id)})
    db.user_restaurants.delete_many({"restaurant_id": ObjectId(id)})
    return {"message": "Success!"}

@blueprint.route("/<id>/favorite", methods=["POST"])
@api_view
@login_required
def favorite_restaurant(id):
    db = app.mongo_client["cs411"]
    is_favorited = db.user_restaurants.find_one({"user_id": session["uid"], "restaurant_id": ObjectId(id)})
    if is_favorited is None:
        db.user_restaurants.insert({
            "user_id": session["uid"],
            "restaurant_id": ObjectId(id)
        })
    else:
        db.user_restaurants.delete_one({
            "user_id": session["uid"],
            "restaurant_id": ObjectId(id)
        })
    return {"status": 200}
