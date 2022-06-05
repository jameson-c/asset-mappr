"""
File: getHospitals.py
Author: Michaela Marincic

Desc: This file gets hospitals across the US from the Community Benefit API:
    - About: https://www.communitybenefitinsight.org/?page=info.data_api
    - API: http://www.communitybenefitinsight.org/api/get_hospitals.php

Finally, the file outputs a pandas dataframe that contains all of the hospital data.


Inputs: Google Places API key, state abbreviation
Output: pandas dataframe Schools, written to .csv
"""
import pandas as pd
import time
import requests
import json
from getAddressCoords_National import getAddressCoords

'''
Func: getHospitals
Input: 
    twoLetterState: The two-letter abbreviation for the state for which we would like to
        pull hospital information.
            
                     
Output: A pandas dataframe containing hospitals in
        our standard format: 
        name	category	vicinity	latitude	longitude	website
'''

def getHealthcare(twoLetterState, APIkey):
    
    stateCode = str(twoLetterState)
    
    url = ('https://npiregistry.cms.hhs.gov/api/?version=2.1')
    params = {
        "version":2.1,
        "enumeration_type":"NPI-2",
        "address_purpose":"LOCATION",
        "city":"Uniontown",
        "state":"PA",
        "limit":200,
        "pretty":True
        }    
print(practAddresses)
    # Call the API
    response = requests.get(url, params=params)
    result = json.loads(response.text)
    df = pd.json_normalize(result['results']) # normalize json file into pandas
    
    if not df.empty: # If there ARE results, continue
        # Healthcare providers with multiple addresses have those addresses stored as sub-tables.
        # Therefore, we need to normalize each of the affiliated addresses
        practLocations = pd.json_normalize(df['practiceLocations'])
        practAddresses = pd.DataFrame()
        for i in range(0,50):
            results = pd.json_normalize(practLocations[i])
            practAddresses = pd.concat([practAddresses,results], axis=1)
            
        df['name'] = df['basic.organization_name']
        df['category'] = 'healthcare'
        df['vicinity'] = df['street_address'] + ', ' + df['city']
        df['address'] = df['street_address'] + ', ' + df['city'] + ', ' + df['state']
        lat = []
        long = []
        for i in df['address']:
            coords = getAddressCoords(i, APIkey)[0]
            lat.append(coords[0])
            long.append(coords[1])
            
        df['latitude'] = lat
        df['longitude'] = long
    
        df = df[['name','category','vicinity','latitude','longitude','website']]
    
        return df
    
    else: # Otherwise, return empty dataframe
        column_names = ['name','category','vicinity','latitude','longitude','website']
        df = pd.DataFrame(columns = column_names)
        return df
        
        