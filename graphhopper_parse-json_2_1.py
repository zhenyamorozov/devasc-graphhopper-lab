# dotenv stuff - TODO remove
import os
from dotenv import load_dotenv # dotenv for convenience
load_dotenv() # dotenv for convenience

import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
loc1 = "Washington, D.C."
loc2 = "Baltimore, Maryland"
key = os.getenv("GRAPHHOPPER_KEY")  ## TODO Replace with your API key

def geocoding (location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?" 
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})

    print("Geocoding API URL for " + location + ":\n" + url)
    json_status = requests.get(url).status_code
    json_data = requests.get(url).json()
    print("Geocoding API URL for " + location + ":\n" + url)
    if json_status == 200:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
    else:
        lat="null"
        lng="null"
    return json_status,lat,lng

orig = geocoding(loc1, key)
print(orig)
dest = geocoding(loc2, key)
print(dest)
