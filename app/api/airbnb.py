import hashlib
from flask import Blueprint, request, current_app as app, session

from app.decorators import api_view, login_required, admin_required

blueprint = Blueprint("api_airbnb", __name__)

@blueprint.route("/", methods=["POST"])
@api_view
@login_required
def add_airbnb():
    db = app.mongo_client["cs411"]
    document = {
        "name": request.form["name"],
        "rating": request.form["rating"],
        "amenities": request.form["amenities"],
        "latitude": request.form["latitude"],
        "longitude": request.form["longitude"],
        "reviews_per_month": request.form["reviews_per_month"],
        "minimum_nights": request.form["minimum_nights"],
        "neighborhood": list(map(str.strip, request.form["neighborhood"].split(","))),
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
            "rating": request.form["rating"],
            "amenities": request.form["amenities"],
            "latitude": request.form["latitude"],
            "longitude": request.form["longitude"],
            "reviews_per_month": request.form["reviews_per_month"],
            "minimum_nights": request.form["minimum_nights"],
            "neighborhood": list(map(str.strip, request.form["neighborhood"].split(","))),
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
