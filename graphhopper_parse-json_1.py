# dotenv stuff - TODO remove
import os
from dotenv import load_dotenv # dotenv for convenience
load_dotenv() # dotenv for convenience

import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
loc1 = "Washington, D.C."
loc2 = "Baltimore, Maryland"
key = os.getenv("GRAPHHOPPER_KEY")  ## TODO Replace with your API key

url = geocode_url + urllib.parse.urlencode({"q":loc1, "limit": "1", "key":key})

json_data = requests.get(url).json()
print(json_data)
