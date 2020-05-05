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
            "rating": airbnb["rating"],
            "amenities": airbnb["amenities"],
            "location": {"type": "Point", "coordinates": [float(airbnb["latitude"]), float(airbnb["longitude"])]},
            "reviews_per_month": airbnb["reviews_per_month"],
            "minimum_nights": airbnb["minimum_nights"],
            "neighborhood": airbnb["neighborhood"],
            "airbnb_url": airbnb["airbnb_url"],
            "image_url": airbnb["image_url"],
            "price": airbnb["price"][1:]
        }
        client["cs411"].airbnb.insert_one(document)
client["cs411"].airbnb.create_index([("location", GEOSPHERE)])
