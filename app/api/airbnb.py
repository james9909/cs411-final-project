from bson.objectid import ObjectId
from flask import Blueprint, request, current_app as app, session

from app.decorators import api_view, login_required, admin_required

blueprint = Blueprint("api_airbnb", __name__)

@blueprint.route("/", methods=["POST"])
@api_view
@admin_required
def add_airbnb():
    db = app.mongo_client["cs411"]
    document = {
        "name": request.form["name"],
        "rating": float(request.form["rating"]),
        "amenities": list(map(str.strip, request.form["amenities"].split(","))),
        "location": {"type": "Point", "coordinates": [float(request.form["latitude"]), float(request.form["longitude"])]},
        "reviews_per_month": float(request.form["reviews_per_month"]),
        "minimum_nights": int(request.form["minimum_nights"]),
        "neighborhood":  request.form["neighborhood"]
    }
    db.airbnb.insert_one(document)
    return {"message": "Success!"}


@blueprint.route("/<id>", methods=["POST"])
@api_view
@admin_required
def update_airbnb(id):
    db = app.mongo_client["cs411"]
    query = {
        "$set": {
            "name": request.form["name"],
            "rating": float(request.form["rating"]),
            "amenities": list(map(str.strip, request.form["amenities"].split(","))),
            "location": {"type": "Point", "coordinates": [float(request.form["latitude"]), float(request.form["longitude"])]},
            "reviews_per_month": float(request.form["reviews_per_month"]),
            "minimum_nights": int(request.form["minimum_nights"]),
            "neighborhood":  request.form["neighborhood"]
        }
    }
    db.airbnb.update_one({"_id": ObjectId(id)}, query)
    return {"message": "Success!"}


@blueprint.route("/<id>", methods=["DELETE"])
@api_view
@admin_required
def delete_airbnb(id):
    db = app.mongo_client["cs411"]
    db.airbnb.delete_one({"_id": ObjectId(id)})
    return {"message": "Success!"}
