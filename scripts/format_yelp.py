import json

BLACKLIST = [
    "Hotels",
    "Medical Centers",
    "Colleges & Universities",
    "Performing Arts",
    "Shipping Centers",
    "Printing Services",
    "Contractors",
    "Radio Stations",
    "Beaches",
    "Swimming Pools",
    "Cinema",
    "Museums",
    "Jewelry",
    "Accessories",
    "Tattoo",
    "Party & Event Planning",
    "General Dentistry",
    "Optometrists",
    "Skin Care",
    "Dermatologists",
    "Eyewear & Opticians",
    "Day Spas",
    "Barbers",
    "Eyelash Service",
    "Hair Salons",
    "Department Stores",
    "Pet Stores",
    "Stadiums & Arenas",
    "Hair Extensions",
    "Wigs",
    "Venues & Event Spaces",
    "Sporting Goods",
    "Tobacco Shops"
]

restaurants = []
with open("data/yelp_restaurants_0-900.json") as f:
    for line in f.readlines():
        data = json.loads(line.strip())
        for business in data.get("businesses", []):
            categories = [c[0] for c in business.get("categories", [])]
            should_skip = False
            for item in BLACKLIST:
                if item in categories:
                    should_skip = True
                    break
            if should_skip:
                continue
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
