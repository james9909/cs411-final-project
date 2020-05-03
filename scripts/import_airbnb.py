import json
import os

from pymongo import MongoClient

client = MongoClient(os.environ["MONGODB_DATABASE_URI"])
client.server_info()

with open("data/listings.json", "r") as f:
    data = json.loads(f.read())

    for airbnb in data[:100]:
        print("Importing {}".format(airbnb["name"]))
        document = {
            "name": airbnb["name"],
            "rating": airbnb["rating"],
            "amenities": airbnb["amenities"],
            "latitude": airbnb["latitude"],
            "longitude": airbnb["longitude"],
            "reviews_per_month": airbnb["reviews_per_month"],
            "minimum_nights": airbnb["minimum_nights"],
            "neighborhood": airbnb["neighborhood"]
        }
        client["cs411"].airbnb.insert_one(document)
