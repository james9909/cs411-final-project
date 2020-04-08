import hashlib

from flask import Blueprint, request, current_app as app, session

from app.decorators import api_view
from app.models import db

blueprint = Blueprint("api_attractions", __name__)

@blueprint.route("/", methods=["GET"])
@api_view
def get_attractions():
	result = db.session.execute("SELECT id, name, address, rating, latitude, longitude FROM attractions").fetchall()
	data = []
	for row in result:
		currDict = {
			"id": row[0],
			"name": row[1],
			"address": row[2],
			"rating": row[3],
			"latitude": row[4],
			"longitude": row[5]
		}
		data.append(currDict)
	return data


@blueprint.route("/", methods=["POST"])
@api_view
def add_attraction():
    name = request.form["name"]
    address = request.form["address"]
    rating = request.form["rating"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]

    db.session.execute("INSERT INTO attractions (name, address, rating, latitude, longitude) VALUES (:name, :address, :rating, :latitude, :longitude)", {
        	"name": name,
			"address": address,
			"rating": rating,
			"latitude": latitude,
			"longitude": longitude
		})
    db.session.commit()
    return {"message": "Success!"}


@blueprint.route("/<id>", methods=["POST"])
@api_view
def update_attractions(id):

    name = request.form["name"]
    address = request.form["address"]
    rating = request.form["rating"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]

    result = db.session.execute("SELECT 1 FROM attractions WHERE id = :id", {"id": id}).fetchone()
    if result is not None:
        db.session.execute("UPDATE attractions SET name = :name, address = :address, rating = :rating, latitude = :latitude, longitude = :longitude WHERE id = :id",
        {
            "id": id,
            "name": name,
            "address": address,
            "rating": rating,
            "latitude": latitude,
            "longitude": longitude
        })
        db.session.commit()
    return {"message": "Success!"}


@blueprint.route("/<id>", methods=["DELETE"])
@api_view
def delete_attractions(id):

	db.session.execute("DELETE FROM attractions WHERE id = :id",
	{
		"id": id
	})
	db.session.commit()
	return {"message": "Success!"}
