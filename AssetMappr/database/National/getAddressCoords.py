"""
File: getAddressCoords
Description: Function to return the coordinates of an input text address
             using the Google Maps geocoding API, and return printed lat-long
             
Problem 1: Typing invalid addresses can still get you a valid lat-long from Google. For example,
           typing 'abc' or 'slkdjflskdjfsdf' will still return a lat-long.
           
Possible solution: bound the retrieved lat-longs to Pittsburgh area? Put some entry constraints on typed address?
       
       
"""

import json
import requests

def getAddressCoords(input_address, api_key):
    params = {'key' : api_key,
              'address' : input_address}
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(url, params)
    result = json.loads(response.text)
    
    # Check these error codes again - there may be more
    if result['status'] not in ['INVALID_REQUEST', 'ZERO_RESULTS']:
                
        lat = result['results'][0]['geometry']['location']['lat']
        long = result['results'][0]['geometry']['location']['lng']
        place_id = result['results'][0]['place_id']

        return [(lat, long), place_id]
    
    # Flagging if there was an error
    else:
        return "Invalid address"