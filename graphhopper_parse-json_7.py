# dotenv stuff - TODO remove
import os
from dotenv import load_dotenv # dotenv for convenience
load_dotenv() # dotenv for convenience

import requests
import urllib.parse

key = os.getenv("GRAPHHOPPER_KEY")  # TODO Replace with your API key

def geocoding (location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit":"1", "key":key})

    response = requests.get(url)
    status_code = response.status_code
    json_data = response.json()
    if status_code == 200 and json_data["hits"]:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        if "state" in json_data["hits"][0]:
            name += ", " + json_data["hits"][0]["state"]

        if "country" in json_data["hits"][0]:
            name += ", " + json_data["hits"][0]["country"]

        print("Geocoding API URL for " + name + " (Location Type: " + value + ")\n" + url)

        return status_code, lat, lng, name
    else:
        if "message" in json_data:
            print("Geocode API status: " + str(status_code) + "\nError message: " + json_data["message"])
        return None


def routing(origin, destination, key):
    if origin and destination:
        op=str(origin[1])+","+str(origin[2])
        dp=str(destination[1])+","+str(destination[2])

        route_url = "https://graphhopper.com/api/1/route?" + urllib.parse.urlencode([
            ("key", key),
            ("vehicle", vehicle),
            ("point", op),
            ("point", dp)
        ])

        response = requests.get(route_url)
        status_code = response.status_code
        json_data = response.json()
        print("Routing API Status: " + str(status_code) + "\nRouting API URL:\n" + route_url)

        if status_code == 200:
            distance = json_data["paths"][0]["distance"]
            time = int(json_data["paths"][0]["time"])
            instructions = json_data["paths"][0]["instructions"]

            return distance, time, instructions
        else:
            print("Error message: " + json_data["message"])
            return None
    else:
        return None


while True:

    profile1=["car", "car_delivery", "car_avoid_ferry", "car_avoid_motorway", "car_avoid_toll"]
    profile2=["truck", "small_truck", "small_truck_delivery","scooter", "scooter_delivery"]
    profile3=["bike", "mtb", "racingbike", "foot", "hike"]

    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print(", ".join(profile1))
    print(", ".join(profile2))
    print(", ".join(profile3))
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    vehicle = input("Enter a vehicle profile from the list above: ")
    if vehicle == "quit" or vehicle == "q":
        break
    elif vehicle not in profile1 + profile2 + profile3:
        vehicle = "car"
        print("No valid vehicle profile was entered. Using the car profile.")

    loc1 = input("Starting Location: ")
    if loc1 == "quit" or loc1 == "q":
        break

    loc2 = input("Destination: ")
    if loc2 == "quit" or loc2 == "q":
        break

    orig = geocoding(loc1, key)
    dest = geocoding(loc2, key)

    path = routing(orig, dest, key)

    print("=================================================")
    if path:
        print("Directions from " + orig[3] + " to " + dest[3] + " by " + vehicle)
        print("-------------------------------------------------")
        miles = path[0]/1000/1.61
        km = path[0]/1000
        sec = int(path[1]/1000%60)
        min = int(path[1]/1000/60%60)
        hr = int(path[1]/1000/60/60)

        print("Distance Traveled: {0:.1f} miles / {1:.1f} km".format(miles, km))
        print("Trip Duration: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
        print("-------------------------------------------------")
        for step in path[2]:
            print("{0} ( {1:.1f} km / {2:.1f} miles )".format(step["text"], step["distance"]/1000, step["distance"]/1000/1.61))
    else:
        print("Route not found")
    print("=================================================")
