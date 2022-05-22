"""
File: getHealthsites.py
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
import coreapi

'''
Func: getHospitals
Input: 
    twoLetterState: The two-letter abbreviation for the state for which we would like to
        pull hospital information.
            
                     
Output: A pandas dataframe containing hospitals in
        our standard format: 
        name	category	vicinity	latitude	longitude	website
'''

def getHealthcare(APIkey):
    
    
    # Initialize a client & load the schema document
    client = coreapi.Client()
    schema = client.get("https://healthsites.io/api/docs/")

    # Interact with the API endpoint
    action = ["api", "v2/facilities/?"]
    params = {
        "api-key": '5b589dc4bee38a9389e67eb883a695ad1eab0828',
        "page": 1,
        #"country": ...,
        #"extent": ...,
        #"output": ...,
        #"from": ...,
        #"to": ...,
        #"flat-properties": ...,
        #"tag-format": ...,
        }
    result = client.action(schema, action, params=params)
    
    #url = ('https://healthsites.io/api/docs/#api-v2-facilities/?api-key=' + 
     #      '5b589dc4bee38a9389e67eb883a695ad1eab0828' + '&page=1')
    
    
    # Call the Community Benefit Insights Hospital Data API
    #response = requests.get(url)
    #result = json.loads(response.text)
    df = pd.json_normalize(result) # normalize json file into pandas
    if not df.empty: # If there ARE results, continue
        # drop unnecessary files, add category column
        # df.drop(['geometry.x', 'geometry.y'],axis = 1)  
        #df['category'] = 'Healthcare'
        #df['website'] = ''
        #df.rename(columns={'street_address' : 'vicinity'})
        #df['vicinity'] = df['street_address'] + ', ' + df['city']
        #df['address'] = df['street_address'] + ', ' + df['city'] + ', ' + df['state']
        #lat = []
        #long = []
        #for i in df['address']:
         #   coords = getAddressCoords(i, APIkey)[0]
          #  lat.append(coords[0])
           # long.append(coords[1])
            
        #df['latitude'] = lat
        #df['longitude'] = long
    
        #df = df[['name','category','vicinity','latitude','longitude','website']]
    
        return df
    
    else: # Otherwise, return empty dataframe
        column_names = ['name','category','vicinity','latitude','longitude','website']
        df = pd.DataFrame(columns = column_names)
        return df
        


print(getHealthcare('5b589dc4bee38a9389e67eb883a695ad1eab0828'))
print(response.text)
