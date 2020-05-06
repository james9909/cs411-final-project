import requests
import json
import os

from bs4 import BeautifulSoup

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

URL = "https://www.google.com/travel/things-to-do/see-all?g2lb=2502548https%3A%2F%2Fwww.google.com%2Ftravel%2Fthings-to-do%2Fsee-all%3Fg2lb%3D2502548%2C4258168%2C4260007%2C4270442%2C4274032%2C4291318%2C4305595%2C4306835%2C4308216%2C4317915%2C4328159%2C4329288%2C4330113%2C4333265%2C4354452%2C4365396%2C4366303%2C4270859%2C4284970%2C4291517%2C4316256%2C4356899&hl=en&gl=us&un=1&otf=1&dest_mid=%2Fm%2F01_d4&dest_state_type=sattd&dest_src=ts&tcfs=EgoKCC9tLzAxX2Q0&sa=X#ttdm=41.882830_-87.620317_14&ttdmf=%252Fm%252F06_7k&hl=en&gl=us&un=1&otf=1&dest_mid=%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252Fm%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252F01_d4&dest_state_type=sattd&dest_src=ts&tcfs=EgoKCC9tLzAxX2Q0&sa=X%252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252523ttdm%25252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525252525253D41.882830_-87.620317_14"

data = []
html = requests.get(URL).text
soup = BeautifulSoup(html, "html.parser")
for attraction in soup.findAll("div", {"class": "Ld2paf"}):
    try:
        info = attraction.find("div", {"class": "GwjAi"})
        name = info.find("div", {"class": ["skFvHc", "YmWhbc"]}).text
        print(name)
        rating = float(info.find("span", {"class": "KFi5wf"}).text)
        num_reviews = int(info.find("span", {"class": "jdzyld"}).text[2:-1].replace(",", ""))
        description = info.find("div", {"class": "nFoFM"}).text
        image_url = attraction.find("img")["data-src"]
        url = "https://maps.googleapis.com/maps/api/geocode/json?address={},+Chicago,+IL&key={}".format(
            name.replace(" ", "+"),
            GOOGLE_API_KEY
        )
        r = requests.get(url).json()
        address = r["results"][0]["formatted_address"]
        loc = r["results"][0]["geometry"]["location"]
        lat = loc["lat"]
        lng = loc["lng"]

        data.append({
            "name": name,
            "rating": rating,
            "num_reviews": num_reviews,
            "description": description,
            "latitude": lat,
            "longitude": lng,
            "address": address,
            "image_url": image_url
        })
    except Exception as e:
        print("Exception: {}".format(e))

with open("data/attractions.json", "w") as f:
    f.write(json.dumps(data))
