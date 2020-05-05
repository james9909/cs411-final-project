import json
import os

from pymongo import MongoClient, GEOSPHERE

client = MongoClient(os.environ["MONGODB_DATABASE_URI"])
client.server_info()

client["cs411"].airbnb.drop()
with open("data/listings.json", "r") as f:
    data = json.loads(f.read())

    for airbnb in data[:100]:
        print("Importing {}".format(airbnb["name"]))
        document = {
            "name": airbnb["name"],
            "rating": int(airbnb["rating"] or "0"),
            "amenities": airbnb["amenities"],
            "location": {"type": "Point", "coordinates": [float(airbnb["latitude"]), float(airbnb["longitude"])]},
            "reviews_per_month": float(airbnb["reviews_per_month"] or 0),
            "minimum_nights": int(airbnb["minimum_nights"] or 1),
            "neighborhood": airbnb["neighborhood"],
            "airbnb_url": airbnb["airbnb_url"],
            "image_url": airbnb["image_url"],
            "price": float(airbnb["price"][1:])
        }
        client["cs411"].airbnb.insert_one(document)
client["cs411"].airbnb.create_index([("location", GEOSPHERE)])
