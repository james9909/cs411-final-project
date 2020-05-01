import json
import requests

seen = set()

with open("data/yelp_restaurants.json", "r") as f:
    data = json.loads(f.read())

    for restaurant in data:
        if restaurant["name"] in seen:
            continue
        print("Importing {}".format(restaurant["name"]))
        r = requests.post("http://localhost:8000/api/restaurants", data={
            "name": restaurant["name"],
            "rating": restaurant["rating"],
            "latitude": restaurant["latitude"],
            "longitude": restaurant["longitude"],
            "address": restaurant["address"],
            "categories": ",".join(restaurant["categories"]),
            "yelp_url": restaurant["yelp_url"]
        })
        assert r.status_code == 200
        seen.add(restaurant["name"])
        if len(seen) == 100:
            break
