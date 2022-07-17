"""
File: getHospitals.py
Author: Michaela Marincic

Desc: This file gets hospitals across the US from the Community Benefit API:
    - About: https://npiregistry.cms.hhs.gov/registry/help-api
    - API: https://npiregistry.cms.hhs.gov/api/demo?version=2.1

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
    
print(newDF)

    # Call the API
    response = requests.get(url, params=params)
    result = json.loads(response.text)
    df = pd.json_normalize(result['results']) # normalize json file into pandas
    
    if not df.empty: # If there ARE results, continue
        # Healthcare providers with multiple addresses have those addresses stored as sub-tables under
        # practiceLocations.
        # Therefore, we need to normalize each of the affiliated addresses
        practLocations = pd.json_normalize(df['practiceLocations'])
        practAddress_1 = pd.json_normalize(practLocations[0])
        practAddress_1['vicinity'] = practAddress_1['address_1'] + ', ' + practAddress_1['city']
        practAddress_1['address'] = practAddress_1['address_1'] + ', ' + practAddress_1['city'] + ', ' + practAddress_1['state']
        practAddress_1 = practAddress_1[['vicinity','address']]
        
        practAddress_2 = pd.json_normalize(practLocations[1])
        practAddress_2['vicinity'] = practAddress_2['address_1'] + ', ' + practAddress_2['city']
        practAddress_2['address'] = practAddress_2['address_1'] + ', ' + practAddress_2['city'] + ', ' + practAddress_2['state']
        practAddress_2 = practAddress_2[['vicinity','address']]
        
        practAddress_3 = pd.json_normalize(practLocations[2])
        practAddress_3['vicinity'] = practAddress_3['address_1'] + ', ' + practAddress_3['city']
        practAddress_3['address'] = practAddress_3['address_1'] + ', ' + practAddress_3['city'] + ', ' + practAddress_3['state']
        practAddress_3 = practAddress_3[['vicinity','address']]
                
        #Pull out the name of each location and assign the category as "healthcare" and website as "".
        df['name'] = df['basic.organization_name']
        df['category'] = 'healthcare'
        df['website'] = ''
    
        df = df[['name','category','website']]
        
        #Concatenate df with each of the 3 practAdress dataframes, then stack all three dataframes.
        
        df1 = pd.concat([df, practAddress_1], axis=1)        
        df2 = pd.concat([df, practAddress_2], axis=1)        
        df3 = pd.concat([df, practAddress_3], axis=1)
        
        newDF = pd.concat([df1, df2, df3])
        newDF = newDF[newDF['address'].notnull()]
        
        #The latitude and longitude will be found by plugging the addresses into Google's API.
        lat = []
        long = []
        for i in newDF['address']:
            coords = getAddressCoords(i, APIkey)[0]
            lat.append(coords[0])
            long.append(coords[1])
            
        newDF['latitude'] = lat
        newDF['longitude'] = long
    
        newDF = newDF[['name','category','vicinity','latitude','longitude','website']]
    
        return newDF
    
    else: # Otherwise, return empty dataframe
        column_names = ['name','category','vicinity','latitude','longitude','website']
        df = pd.DataFrame(columns = column_names)
        return df
        
        