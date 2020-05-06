import hashlib

from flask import Blueprint, request, current_app as app, session

from app.decorators import api_view, login_required, admin_required
from app.models import db

blueprint = Blueprint("api_attractions", __name__)

@blueprint.route("/", methods=["GET"])
@api_view
@login_required
def get_attractions():
    result = db.session.execute("SELECT id, name, address, rating, latitude, longitude, image_url FROM attractions").fetchall()
    data = []
    for row in result:
        currDict = {
            "id": row[0],
            "name": row[1],
            "address": row[2],
            "rating": row[3],
            "latitude": row[4],
            "longitude": row[5],
            "image_url": row[6]
        }
        data.append(currDict)
    return {
        "status": 200,
        "data": data
    }


@blueprint.route("/", methods=["POST"])
@api_view
@admin_required
def add_attraction():
    name = request.form["name"]
    address = request.form["address"]
    rating = request.form["rating"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]
    image_url = request.form["image_url"]

    db.session.execute("INSERT INTO attractions (name, address, rating, latitude, longitude, image_url) VALUES (:name, :address, :rating, :latitude, :longitude, :image_url)", {
        "name": name,
        "address": address,
        "rating": rating,
        "latitude": latitude,
        "longitude": longitude,
        "image_url": image_url
    })
    db.session.commit()
    return {"status": 200, "message": "Attraction added"}


@blueprint.route("/<id>", methods=["POST"])
@api_view
@admin_required
def update_attractions(id):
    name = request.form["name"]
    address = request.form["address"]
    rating = request.form["rating"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]
    image_url = request.form["image_url"]

    result = db.session.execute("SELECT 1 FROM attractions WHERE id = :id", {"id": id}).fetchone()
    if result is None:
        return {"status": 404, "message": "Attraction not found"}

    db.session.execute("UPDATE attractions SET name = :name, address = :address, rating = :rating, latitude = :latitude, longitude = :longitude, image_url = :image_url WHERE id = :id",
    {
        "id": id,
        "name": name,
        "address": address,
        "rating": rating,
        "latitude": latitude,
        "longitude": longitude,
        "image_url": image_url
    })
    db.session.commit()
    return {"status": 200, "message": "Attraction updated"}


@blueprint.route("/<id>", methods=["DELETE"])
@api_view
@admin_required
def delete_attractions(id):
    db.session.execute("DELETE FROM attractions WHERE id = :id", {"id": id})
    db.session.execute("DELETE FROM user_attractions WHERE attraction_id = :id", {"id": id})
    db.session.commit()
    return {"status": 200, "message": "Attraction deleted"}

@blueprint.route("/<id>/favorite", methods=["POST"])
@api_view
@login_required
def favorite_attraction(id):
    result = db.session.execute("SELECT 1 FROM attractions WHERE id = :id", {"id": id}).fetchone()
    if result is None:
        return {"status": 404, "message": "Attraction not found"}

    is_favorited = db.session.execute("SELECT 1 FROM user_attractions WHERE user_id = :user_id AND attraction_id = :attraction_id", {
        "user_id": session["uid"],
        "attraction_id": id
    }).fetchone()
    if is_favorited is None:
        db.session.execute("INSERT INTO user_attractions (user_id, attraction_id) VALUES (:user_id, :attraction_id)", {
            "user_id": session["uid"],
            "attraction_id": id
        })
    else:
        db.session.execute("DELETE FROM user_attractions WHERE user_id = :user_id AND attraction_id = :attraction_id", {
            "user_id": session["uid"],
            "attraction_id": id
        })
    db.session.commit()
    return {"status": 200}
