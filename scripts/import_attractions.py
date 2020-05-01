import json
import requests

with open("data/attractions.json", "r") as f:
    data = json.loads(f.read())

    for attraction in data:
        print("Importing {}".format(attraction["name"]))
        r = requests.post("http://localhost:8000/api/attractions", data={
            "name": attraction["name"],
            "address": attraction["address"],
            "rating": attraction["rating"],
            "latitude": attraction["latitude"],
            "longitude": attraction["longitude"],
        })
        assert r.status_code == 200
