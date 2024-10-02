import os
import requests

key = os.getenv('GRAPHHOPPER_KEY')
base_url = 'https://graphhopper.com/api/1'

def geocode(location):
    '''
    Retrieves the coordinates for a given location string
    Returns coordinates as a list: [lat, lon]
    '''
    # Prepare the parameters for request
    params = {
        'key': key,
        'q': location
    }
    
    # Perform the request
    resp = requests.get(
        base_url + '/geocode',
        params=params
    )

    # Check if request was succesful
    if resp.status_code != 200:
        return

    resp_data = resp.json()

    # Check if result is empty
    if len(resp_data['hits']) == 0:
        return
    
    lat = resp_data['hits'][0]['point']['lat']
    lon = resp_data['hits'][0]['point']['lng']

    coords = [lat, lon]

    return coords


def route(origin, destination):
    '''
    Retrieves a route between two given points.
    Expects points as a list of floats: [lat, lon]
    Returns: a dict with keys TODO
    '''

    # Prepare request parameters
    params = {
        'key': key,
        'point': [
            f"{origin[0]}, {origin[1]}", 
            f"{destination[0]}, {destination[1]}", 
        ]
    }

    # Perform the routing request
    resp = requests.get(
        base_url + '/route',
        params=params
    )

    # Check if request was succesful 
    if resp.status_code != 200:
        return

    resp_data = resp.json()

    result = {
        'distance': resp_data['paths'][0]['distance'],
        'time': resp_data['paths'][0]['time'],
        'instructions': [f"{instruction['text']} for {instruction['distance']/1000:.2f} km" for instruction in resp_data['paths'][0]['instructions']]
    }

    return result


point_a = geocode('Berlin')
point_b = geocode('Munchen')
print(route(point_a, point_b))

