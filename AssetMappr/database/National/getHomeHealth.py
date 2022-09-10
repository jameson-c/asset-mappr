"""
File: getHomeHealth.py
Author: Michaela Marincic

Desc: This file gets hospitals across the US from the Community Benefit API:
    - About: https://data.cms.gov/provider-data/dataset/6jpm-sxkc
    - API: ​/provider-data​/api​/1​/datastore​/sql

Finally, the file outputs a pandas dataframe that contains all of the home health service data.


Inputs: Google Places API key, state-county code abbreviation 
Output: pandas dataframe df returned
"""
import pandas as pd
import requests
import json
from getAddressCoords import getAddressCoords

'''
Func: getHomeHealth
Input: 
    twoLetterState: 2-letter state abbreviation
    CountyFIPS: The 5-number state and county for which we would like to
        pull hospital information. https://www.nrcs.usda.gov/wps/portal/nrcs/detail/pa/home/?cid=nrcs143_013697
    APIkey: a google places API key necessary to run the address search
            
                     
Output: A pandas dataframe containing hospitals in
        our standard format: 
        name	category	description address	latitude	longitude	website
'''

def getHomeHealth(twoLetterState, APIkey):
    
    twoLetterState = str(twoLetterState)
    
    url = ('https://data.cms.gov/provider-data/api/1/datastore/sql?query=%5BSELECT%20%2A%20FROM%2047901c55-456c-5e4e-a79a-f648f26985c8%5D%5BWHERE%20State%20%3D%20%22PA%22%5D%5BLIMIT%202%5D')
    
    # Call the Community Benefit Insights Hospital Data API
    response = requests.get(url)
    result = json.loads(response.text)
    df = pd.json_normalize(result) # normalize json file into pandas
    print(df)
    if not df.empty: # If there ARE results, continue
        # drop hospitals outside of the county we are viewing
        df = df.drop(df.loc[df['fips_state_and_county_code']!=CountyFIPS].index)
        
        df['category'] = 'Healthcare'
        df['description'] = 'Hospital'
        df['asset_name'] = df['name']
        df['website'] = ''
        df['source_type'] = 'Community Benefit Hospitals API'
        df.rename(columns={'street_address' : 'vicinity'})
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
    
        df = df[['asset_name','category','description','address','latitude','longitude','website','source_type']]
    
        return df
    
    else: # Otherwise, return empty dataframe
        column_names = ['asset_name','category','description','address','latitude','longitude','website', 'source_type']
        df = pd.DataFrame(columns = column_names)
        return df
    