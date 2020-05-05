import os
import json
import requests

from pymongo import MongoClient, GEOSPHERE

seen = set()

client = MongoClient(os.environ["MONGODB_DATABASE_URI"])
client.server_info()

client["cs411"].restaurants.drop()
with open("data/yelp_restaurants.json", "r") as f:
    data = json.loads(f.read())

    for restaurant in data:
        if restaurant["name"] in seen:
            continue
        print("Importing {}".format(restaurant["name"]))
        client["cs411"].restaurants.insert_one({
            "name": restaurant["name"],
            "rating": restaurant["rating"],
            "location": {"type": "Point", "coordinates": [restaurant["latitude"], restaurant["longitude"]]},
            "address": restaurant["address"],
            "categories": restaurant["categories"],
            "yelp_url": restaurant["yelp_url"]
        })
        seen.add(restaurant["name"])
        if len(seen) == 150:
            break

client["cs411"].restaurants.create_index([("location", GEOSPHERE)])
