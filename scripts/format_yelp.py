import json

restaurants = []
with open("data/yelp_restaurants_0-900.json") as f:
    for line in f.readlines():
        data = json.loads(line.strip())
        for business in data.get("businesses", []):
            categories = [c[0] for c in business.get("categories", [])]
            try:
                address = "{}, {}, {} {}".format(
                    business["location"]["address"][0],
                    business["location"]["city"],
                    business["location"]["state_code"],
                    business["location"]["postal_code"],
                )
                restaurants.append({
                    "name": business["name"],
                    "rating": business["rating"],
                    "categories": categories,
                    "latitude": business["location"]["coordinate"]["latitude"],
                    "longitude": business["location"]["coordinate"]["longitude"],
                    "address": address,
                    "yelp_url": business["url"]
                })
            except Exception as e:
                pass

with open("data/yelp_restaurants.json", "w") as f:
    f.write(json.dumps(restaurants))
print(len(restaurants))
